#!/usr/bin/env python3
"""Hybrid metadata extraction: PDF text-layer (PUA-decoded) + Haiku.

Sonnet vision via claude CLI averaged 100-360s per problem (Read-tool
+ tool-turn overhead). PDF text-layer + Haiku averages 3-5s — 50× faster
at < 1/6 the cost, and the text-layer is 100% accurate for the parts
Haiku needs (Korean body, problem number, area header). The PNG remains
the user-facing body, so figure quality is unaffected; metadata
classification just doesn't need vision.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
from ingest_round import claude_p, load_concept_index, scope_for, validate_mapping  # noqa: E402


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


# EBSi / KICE PUA digit glyphs:   → 1..9,  → 0
_PUA_DIGIT_MAP = {0xe034 + i: ord(str(i + 1)) for i in range(9)}
_PUA_DIGIT_MAP[0xe03d] = ord('0')


META_SYSTEM = """너는 한국 수능 수학 기출문제 분류 전문가다.

입력은 한 문제의 PDF text-layer 추출이다. 일부 수식 글리프(예: \\ue0fc)는
표현 불가능해 그대로 남아있을 수 있다 — 글리프 자체 해석은 무시하고
한국어 본문 + 숫자 + 명백한 변수 이름만으로 의미를 파악하라.

다음 JSON을 출력하라:

{
  "searchable_text": "본문을 자연스럽게 옮긴 한국어 + LaTeX. 객관식(5지선다)이면 선택지 ①②③④⑤를 각각의 값·식과 함께 모두 포함(솔버 검증·유사문제 재생성에 필수)",
  "format": "choice" 또는 "numeric"   # 5지선다면 choice, 단답형이면 numeric
  "has_figure": true 또는 false   # 본문에 [그림] 또는 도형 언급이 있으면 true
  "unit": "단원 slug — 아래 단원 목록 중 하나",
  "concepts": ["관련 spoke 1", "spoke 2"]  # unit 하위 spoke 1-4개 (모르면 빈 배열)
  "exam_intent": "이 문제의 출제 의도 한 문장 (50자 이내)",
  "killer_tier": "early" / "mid" / "killer"
  "cognitive_type": "계산" / "개념" / "응용" / "추론" / "통합"
}

killer_tier:
- early: 1-15번 수준 (2-3점)
- mid: 16-22번 또는 23-27번 (3-4점)
- killer: 21-22, 28-30 같은 최고난도 (4점)

오직 JSON. 코드펜스/주석/설명 금지."""


def _extract_problem_text(pdf_path: Path, page_num: int, bbox_pdf: tuple) -> str:
    """문제 영역 본문 추출. hancom_decode 기하 구조복원(로제타+분수·지수·첨자·cases·근호)을
    먼저 시도(한컴 PUA 수식을 ⋄로 폐기하던 옛 로직 대체) → 실패 시 fitz+PUA-digit 폴백."""
    try:
        import hancom_decode as _hd
        _t = _hd.decode_problem(str(pdf_path), page_num, bbox_pdf)
        if _t and len(_t.strip()) >= 8:
            return _t.strip()
    except Exception:
        pass
    try:
        d = fitz.open(pdf_path)
        if page_num - 1 >= len(d):
            d.close()
            return ''
        page = d[page_num - 1]
        # Clip to bbox; PyMuPDF returns text whose origin is inside the rect.
        x0, y0, x1, y1 = bbox_pdf
        rect = fitz.Rect(x0, y0, x1, y1)
        raw = page.get_text(clip=rect)
        d.close()
    except Exception:
        return ''
    # PUA digit decode
    decoded = raw.translate(_PUA_DIGIT_MAP)
    # Collapse runs of unicode PUA glyphs (수식 잔재) to single ⋄ marker —
    # the classifier ignores them but keeps the textual flow readable.
    decoded = re.sub(r'[-]+', '⋄', decoded)
    # Normalize whitespace (preserve line breaks for readability)
    decoded = re.sub(r'[ \t]+', ' ', decoded)
    decoded = re.sub(r'\n{3,}', '\n\n', decoded)
    return decoded.strip()


def extract_metadata(pdf_path: Path, page_num: int, bbox_pdf: tuple,
                     number: int, subject: str,
                     units_index: dict[str, list[str]],
                     cache_dir: Path | None = None,
                     cache_key: str | None = None,
                     timeout: int = 60,
                     image_path: Path | None = None,
                     grade: str | None = None,
                     year: int | None = None,
                     model: str = 'sonnet') -> dict | None:
    """문제 1개의 메타데이터. **개념 매핑은 이미지 직독 + 스코프 + 게이트**를 거친다.

    ★2026-08-13 개편. 이전에는 여기서 단원 **이름만** 나열하고 concepts 는 "unit 하위
      spoke 1-4개" 라고 말로만 요구했다 — 스포크는 사실상 **창작**이었고 게이트가 없어
      지어낸 개념이 그대로 frontmatter 로 나가 stub 을 양산했다(평면 개념 274개의 출처).
      게다가 입력이 PDF 텍스트레이어라 지수가 근호로 뭉개져(4^(2/3) → 4√3/2) 수능 문제가
      중3 무리수 문제로 보였다.

    ★그래서 매핑 본체는 run_stage1.map_problem_once **한 벌만** 쓴다. 오늘 load_concept_index
      가 두 벌이라 각각 다른 이유로 같은 사고를 냈다 — 구현이 갈리면 반드시 어긋난다.

    ★searchable_text 는 여전히 PDF 텍스트에서 뽑는다(검색·본문용). 다만 **개념 매핑의
      근거로는 쓰지 않는다** — 손상된 텍스트가 판단을 끌어당기기 때문이다.

    cache_key: stable filename stem. 캐시는 텍스트 sha + **스코프 지문**으로 무효화된다 —
    스코프가 바뀌었는데 옛 캐시를 재사용하면 고친 규칙이 적용되지 않는다.
    """
    body_text = _extract_problem_text(pdf_path, page_num, bbox_pdf)
    if not body_text:
        return None

    scope = scope_for(subject, grade, is_high=bool(year and int(year) >= 2019), year=year)
    index = load_concept_index(scope) if scope else (units_index or load_concept_index())
    if not index:
        print(f'  ! #{number} {subject}: 개념 후보 0개 — 매핑 중단(스코프/경로 확인)', flush=True)
        return None

    scope_sig = hashlib.sha1(('|'.join(sorted(index))).encode()).hexdigest()[:8]
    text_sha = hashlib.sha1((body_text + scope_sig).encode('utf-8')).hexdigest()[:12]
    cache_file = None
    if cache_dir and cache_key:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f'{cache_key}.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text(encoding='utf-8'))
                if data.get('text_sha') == text_sha and isinstance(data.get('meta'), dict):
                    return _normalize(data['meta'])
            except Exception:
                pass

    # ── 개념 매핑: 이미지가 있으면 공용 매퍼(이미지 직독 + 스포크 목록 + 게이트) ──────
    if image_path and Path(image_path).exists():
        from run_stage1 import map_problem_once   # 지연 import — 순환 방지
        mapped = map_problem_once('', number, 0, index, subject=subject, grade=grade,
                                  model=model, image=image_path)
        if mapped and mapped.get('unit'):
            ok, why = validate_mapping(mapped['unit'], mapped.get('concepts'), index)
            if not ok:
                allowed = set(index.get(mapped['unit'], []))
                mapped['concepts'] = [c for c in (mapped.get('concepts') or []) if c in allowed]
                print(f'  ~ #{number} {subject}: 후보 밖 개념 정리 ({why})', flush=True)
            normalized = _normalize(mapped)
            normalized['searchable_text'] = body_text[:3000]
            if cache_file:
                try:
                    cache_file.write_text(
                        json.dumps({'text_sha': text_sha, 'meta': normalized}, ensure_ascii=False, indent=2),
                        encoding='utf-8')
                except Exception:
                    pass
            return normalized
        print(f'  ! #{number} {subject}: 이미지 매핑 실패 — 텍스트로 폴백', flush=True)

    # ── 폴백: 텍스트 기반. 이때도 **스포크 목록과 게이트**는 건다 ────────────────────
    units_str = '\n'.join(f'- {u}' for u in sorted(index))
    spokes_str = '\n'.join(f'  · {c}' for u in sorted(index) for c in sorted(index[u])[:6])
    base_user = f"""문제 번호: {number}, 영역: {subject}

사용 가능한 단원(경로 그대로 하나 선택):
{units_str}

각 단원의 개념 일부(concepts 는 반드시 이 형식의 **경로**로, 목록 밖은 지어내지 마라):
{spokes_str[:6000]}

본문 (PDF text-layer, PUA digits decoded, 수식 글리프는 ⋄):
{body_text[:3000]}

사용 가능한 unit (이 중 하나 선택):
{units_str}

위 JSON을 출력하라."""

    last_err = None
    for attempt in range(3):
        user = base_user
        if attempt > 0:
            user += '\n\n중요: 오직 JSON 객체 하나만 출력. 코드펜스/주석 금지.'
        out = claude_p(META_SYSTEM, user, model='haiku', max_turns=1,
                       timeout=timeout, retries=1)
        if not out:
            last_err = 'empty response'
            continue
        out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
        try:
            parsed = json.loads(out)
        except Exception as e:
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
            last_err = f'non-dict (try {attempt+1})'
            continue
        normalized = _normalize(parsed)
        # ★텍스트 폴백에도 게이트를 건다 — 지어낸 개념이 frontmatter 로 나가면 stub 이 생긴다.
        ok, why = validate_mapping(normalized.get('unit'), normalized.get('concepts'), index)
        if not ok:
            allowed = set(index.get(normalized.get('unit') or '', []))
            normalized['concepts'] = [c for c in (normalized.get('concepts') or []) if c in allowed]
        # searchable_text 는 기하 디코드(정확)를 그대로 사용 — Haiku 재작성 환각 방지.
        # (Haiku 는 format/tier/unit 분류용으로만 신뢰)
        normalized['searchable_text'] = body_text[:3000]
        if cache_file:
            try:
                cache_file.write_text(
                    json.dumps({'text_sha': text_sha, 'meta': normalized}, ensure_ascii=False, indent=2),
                    encoding='utf-8',
                )
            except Exception:
                pass
        return normalized

    print(f'  ! text_meta gave up for #{number} {subject} after 3 attempts: {last_err}', flush=True)
    return None


_ALLOWED_FORMAT = {'choice', 'numeric'}
_ALLOWED_TIER = {'early', 'mid', 'killer'}
_ALLOWED_COG = {'계산', '개념', '응용', '추론', '통합'}


def _normalize(meta: dict) -> dict:
    out: dict = {}
    out['searchable_text'] = str(meta.get('searchable_text', '')).strip()
    fmt = str(meta.get('format', '')).strip().lower()
    out['format'] = fmt if fmt in _ALLOWED_FORMAT else 'numeric'
    out['has_figure'] = bool(meta.get('has_figure', False))
    # slugs use underscores; Haiku sometimes returns spaces — normalize.
    def _slugify(s: str) -> str:
        return s.strip().replace(' ', '_')
    out['unit'] = _slugify(str(meta.get('unit', ''))) or None
    concepts = meta.get('concepts', [])
    if isinstance(concepts, list):
        out['concepts'] = [_slugify(str(c)) for c in concepts if str(c).strip()][:6]
    else:
        out['concepts'] = []
    out['exam_intent'] = str(meta.get('exam_intent', '')).strip()[:200]

    def _pick(val, allowed):
        if not val:
            return None
        s = str(val).strip()
        if s in allowed:
            return s
        for tok in re.split(r'[|,/、]', s):
            tok = tok.strip()
            if tok in allowed:
                return tok
        return None
    out['killer_tier'] = _pick(meta.get('killer_tier'), _ALLOWED_TIER)
    out['cognitive_type'] = _pick(meta.get('cognitive_type'), _ALLOWED_COG)
    return out
