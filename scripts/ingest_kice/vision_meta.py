#!/usr/bin/env python3
"""Per-problem metadata extraction via Claude Sonnet 4.6 vision.

Input: cropped problem PNG (from bbox.crop_problem_image)
Output: JSON metadata dict — searchable_text, unit/concepts/etc.

Replaces the OCR-then-Haiku-classify path. Sonnet sees the actual rendered
PDF region (including any figures, formulas in their original glyph form)
so it can:
  - transcribe the body into Korean plain text + LaTeX (for search index)
  - classify unit/concepts using the LWIP concept tree
  - judge difficulty and expected time
  - detect whether the problem has a figure (PNG already contains it, but
    this flag helps filter/search later)

Cache: db/raw/{slug}/meta_cache/{subject}_{number:02d}.json  (sha1 of image)
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
import subprocess
import time
from pathlib import Path

_SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(_SCRIPTS / 'ingest_kice'))
sys.path.insert(0, str(_SCRIPTS))
try:
    from ingest_round import claude_p, load_concept_index  # type: ignore
    from tiers import ALLOWED_COG, ALLOWED_TIER, TIER_GUIDE, pick_enum  # type: ignore  # 어휘 정본
    from tiling import vision_paths  # 큰 문제는 타일로 분할해 vision 입력(통PNG는 vision 다운스케일로 글자 뭉개짐 → 빈응답/타임아웃)
except Exception as e:
    print(f'failed to import claude_p / load_concept_index / vision_paths: {e}', file=sys.stderr)
    raise


def _first_json_object(s: str) -> str | None:
    """Return the first balanced {...} object in s (string/escape aware).

    Tolerant of trailing prose after the closing brace and of nested braces
    inside the object — unlike the lazy lookahead regex which only recovers an
    object that is the very last token of the output.
    """
    start = s.find('{')
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(s)):
        c = s[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
    return None


VISION_SYSTEM = """너는 한국 수능 수학 기출문제 분류 전문가다. 주어진 PNG 이미지는
PDF에서 잘라낸 문제 하나의 영역이다 (본문 + 보기 + 그림이 모두 포함됨).

이미지를 Read 툴로 열어 다음 JSON을 출력하라:

{
  "searchable_text": "문제 본문을 한국어 plain text + LaTeX로 정확히 옮긴 것. 보기는 ①②③④⑤로 구분. 줄바꿈 보존.",
  "format": "choice" 또는 "numeric",
  "has_figure": true 또는 false,
  "unit": "단원 slug — 아래 단원 목록 중 하나",
  "concepts": ["spoke slug 1", "spoke slug 2"],
  "exam_intent": "이 문제의 출제 의도 한 문장 (50자 이내, 무엇을 묻는지)",
  "killer_tier": "early" / "mid" / "high" / "killer",
  "cognitive_type": "계산" / "개념" / "응용" / "추론" / "통합",
  "expected_time_sec": 60-1800 사이 정수,
  "figure_spec": null  // has_figure=true 면서 우리 spec으로 표현 가능한 도형이면 아래 형식
}

=== figure_spec (선택, has_figure=true 일 때만) ===

도형이 우리 컴포넌트로 표현 가능하면 채운다. 불가능하면 null.

- 함수 그래프 (포물선/지수/로그/삼각/유리/무리):
  {"kind": "plot", "spec": {"fn": "x^2 - 2*x", "range": [-3, 5], "points": [{"at":[1,-1]}]}, "confidence": 0.8}

- 평면도형 (삼각형/원/사각형/접선/보조선):
  {"kind": "geometry", "spec": {"shapes": [
    {"kind":"point","at":[2,3],"label":"A"},
    {"kind":"segment","from":[0,0],"to":[2,3],"label":"AB"},
    {"kind":"circle","center":[0,0],"r":2}
  ]}, "confidence": 0.7}

- 수직선 위 부등식/구간:
  {"kind": "numberline", "spec": {"range":[-5,5], "marks":[{"at":2,"closed":false}], "intervals":[{"from":-3,"to":2,"closed":[true,false]}]}, "confidence": 0.9}

- 통계 차트 (히스토그램/표):
  {"kind": "chart", "spec": {"kind":"hist", "bins":[...], "freq":[...]}, "confidence": 0.6}

confidence < 0.5 이거나 표현 어려우면 figure_spec=null. searchable_text 의 [그림: ...] 묘사가 fallback.

""" + TIER_GUIDE + """

=== searchable_text 작성 규칙 (중요) ===

1. **모든 수식을 LaTeX `$...$`로 정확히 옮긴다.** `⋄`, `□`, `?`, 'placeholder' 같은
   기호를 절대 쓰지 말 것. 글리프가 잘 안 보이면 인접 문맥(보기·이어지는 문장)
   으로 추정해 최소 그럴듯한 수식을 작성. 분수는 `\\dfrac{a}{b}`, 거듭제곱은
   `x^{n+1}`, 적분 `\\int_a^b`, 합 `\\sum_{k=1}^n` 등 KaTeX 호환 표기.

2. **도형이 있으면 (has_figure=true) 도형을 텍스트로 묘사한다.** `[그림]` 같은
   placeholder 절대 금지. 다음 항목을 그림 묘사 끝에 `[그림: ...]` 형식으로 포함:
   - 좌표 (예: $A(2,3)$, 원점 $O$, 점 $P$가 곡선 위에)
   - 각도/길이 (예: $\\angle OAB = \\theta$, $\\overline{AB}=5$)
   - 도형 종류 (삼각형/원/부채꼴/포물선/접선/보조선)
   - 보조선·교점·표시(빗금 영역, 음영)
   - 그래프 함수식 + 교점·점근선
   - 좌표축 라벨, 단위
   이 텍스트만으로 도형 위치·관계를 재구성할 수 있어야 한다.

3. **이미지 일부가 잘리거나 흐려도** 보이는 범위 내에서 정확한 부분만 옮기고,
   불확실한 부분은 명시 (예: `[하단 일부 잘림: 선택지 ⑤ 식 불확실]`).

4. **인접 문제와 섞이지 않게**, 현재 문제 번호 "N."로 시작하는 본문 + 그 보기까지
   만 옮긴다. 다음 문제 본문이 같은 영역에 들어와 있으면 무시.

5. **본문 길이는 50-1200자 정도.** 너무 짧으면 OCR 누락 가능성, 너무 길면 인접
   문제 cross-contamination 의심 — 신중히 자르기.

오직 JSON만 출력. 코드펜스/주석/설명 금지."""


def _sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:12]


def _format_units_for_prompt(units_index: dict[str, list[str]]) -> str:
    """Compact: unit names only. Spokes were dumped in full earlier but
    they balloon the prompt to ~6KB which slows Sonnet vision noticeably.
    Sonnet knows Korean math curriculum well enough to pick relevant
    spokes from the unit name + problem context."""
    return ', '.join(sorted(units_index.keys()))


def extract_metadata(image_path: Path, units_index: dict[str, list[str]],
                     cache_dir: Path | None = None,
                     timeout: int = 60) -> dict | None:
    """Call Sonnet 4.6 vision on a cropped problem PNG. Returns parsed JSON
    or None on persistent failure. Caches by image sha1 in cache_dir.

    Cache hit returns immediately. Cache miss → 3 retries with prompt
    tightening on JSON parse errors."""
    sha = _sha1_of_file(image_path)
    cache_file = None
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f'{image_path.stem}.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text(encoding='utf-8'))
                if data.get('sha') == sha and isinstance(data.get('meta'), dict):
                    return _normalize(data['meta'])
            except Exception:
                pass

    units_str = _format_units_for_prompt(units_index)
    tiles, is_tiled = vision_paths(image_path)   # 큰 문제는 타일로 분할(통PNG 다운스케일 방지)
    if is_tiled:
        listing = '\n'.join(f'  {i + 1}. {t.absolute()}' for i, t in enumerate(tiles))
        img_ref = (f"이 문제는 세로로 긴 이미지라 {len(tiles)}개 타일로 분할돼 있다. 아래 타일을 "
                   f"위→아래 순서로 **모두** Read 해 하나의 연속된 문제로 이어붙여 읽어라"
                   f"(타일 경계는 약간 겹쳐 있으니 중복 내용은 무시):\n{listing}")
        add_dir = str(tiles[0].absolute().parent)
    else:
        img_ref = f'이미지: {image_path.absolute()}'
        add_dir = str(image_path.absolute().parent)
    base_user = f"""{img_ref}

사용 가능한 unit (이 중 하나를 선택):
{units_str}

위 JSON을 출력하라."""
    last_err = None
    for attempt in range(3):
        user = base_user
        if attempt > 0:
            user += '\n\n중요: 오직 JSON 객체 하나만 출력. 코드펜스/주석/추가 텍스트 모두 금지.'
        out = claude_p(VISION_SYSTEM, user, model='sonnet', max_turns=3,
                       add_dir=add_dir, timeout=timeout, retries=1)
        if not out:
            last_err = 'empty response'
            continue
        out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
        try:
            parsed = json.loads(out)
        except Exception as e:
            # salvage: first balanced {...} block (tolerant of trailing prose)
            salvaged = _first_json_object(out)
            if salvaged is not None:
                try:
                    parsed = json.loads(salvaged)
                except Exception as e2:
                    last_err = f'parse fail (try {attempt+1}): {e}; salvage: {e2}'
                    continue
            else:
                last_err = f'parse fail (try {attempt+1}): {e}'
                continue
        if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
            parsed = parsed[0]
        if not isinstance(parsed, dict):
            last_err = f'non-dict (try {attempt+1}): {type(parsed).__name__}'
            continue
        # success
        normalized = _normalize(parsed)
        if cache_file:
            try:
                cache_file.write_text(
                    json.dumps({'sha': sha, 'meta': normalized}, ensure_ascii=False, indent=2),
                    encoding='utf-8',
                )
            except Exception:
                pass
        return normalized

    print(f'  ! vision_meta gave up for {image_path.name} after 3 attempts: {last_err}', flush=True)
    return None


_ALLOWED_FORMAT = {'choice', 'numeric'}
# 난이도·인지유형 어휘는 tiers.py 정본(ALLOWED_TIER/ALLOWED_COG)을 쓴다 — 여기 다시 적지 않는다.


def _normalize(meta: dict) -> dict:
    """Coerce LLM output into the schema used downstream. Drop bogus values
    so DB constraints don't trip later."""
    out: dict = {}
    out['searchable_text'] = str(meta.get('searchable_text', '')).strip()
    fmt = str(meta.get('format', '')).strip().lower()
    out['format'] = fmt if fmt in _ALLOWED_FORMAT else 'numeric'
    out['has_figure'] = bool(meta.get('has_figure', False))
    out['unit'] = str(meta.get('unit', '')).strip() or None
    concepts = meta.get('concepts', [])
    if isinstance(concepts, list):
        out['concepts'] = [str(c).strip() for c in concepts if str(c).strip()][:6]
    else:
        out['concepts'] = []
    out['exam_intent'] = str(meta.get('exam_intent', '')).strip()[:200]

    out['killer_tier'] = pick_enum(meta.get('killer_tier'), ALLOWED_TIER, 'killer_tier')
    out['cognitive_type'] = pick_enum(meta.get('cognitive_type'), ALLOWED_COG, 'cognitive_type')
    try:
        et = int(meta.get('expected_time_sec', 0))
        out['expected_time_sec'] = max(60, min(1800, et)) if et else None
    except Exception:
        out['expected_time_sec'] = None
    return out


if __name__ == '__main__':
    # Smoke test on one image
    if len(sys.argv) < 2:
        print('usage: vision_meta.py <image_path>')
        sys.exit(1)
    img = Path(sys.argv[1])
    units = load_concept_index()
    print(f'units: {len(units)}')
    print(f'image: {img}')
    t0 = time.time()
    result = extract_metadata(img, units)
    print(f'\n=== result ({time.time()-t0:.1f}s) ===')
    print(json.dumps(result, ensure_ascii=False, indent=2))
