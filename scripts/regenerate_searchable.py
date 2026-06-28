#!/usr/bin/env python3
"""빈칸추론형 searchable_text 전체 재생성 (이미지→충실 전사). 재대조 결과 90% 결함 → 통째 교체.
이미지=정답. Sonnet에게 충실 전사 받아 frontmatter의 searchable_text 블록만 교체.
정답·검증기·풀이는 안 건드림(전부 이미지 파생이라 정확). 멱등: 매 실행 재생성(덮어쓰기).
환경: REGEN_LIMIT(0=전체), REGEN_MODEL(sonnet), REGEN_TO(220), REGEN_WORKERS(4)."""
from __future__ import annotations
import re, sys, json, glob, os, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

MODEL = os.environ.get('REGEN_MODEL', 'sonnet')
TO = int(os.environ.get('REGEN_TO', '220'))
WORKERS = int(os.environ.get('REGEN_WORKERS', '4'))
LIMIT = int(os.environ.get('REGEN_LIMIT', '0'))
# ★프롬프트 캐싱 위생: clean cwd(벨트) + DISABLE_GIT(멜빵). 타일은 --add-dir(절대경로)라 cwd 무관.
_CLEAN_DIR = os.environ.get('CLAUDE_P_CWD', '/tmp/claude_p_clean')
os.makedirs(_CLEAN_DIR, exist_ok=True)
_CLAUDE_ENV = {**os.environ, 'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS': '1'}
SYSTEM = ("당신은 한국 수능 수학 문제를 한 글자도 틀리지 않게 전사하는 전문가입니다. "
          "첨부 이미지가 유일한 근거입니다. 추측·생략·창작 절대 금지.")


def extract(t):
    m = re.search(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', t, re.M | re.S)
    return m.group(1).strip() if m else ''


def prompt_for(tiles):
    listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))
    return (f"문제 이미지(여러 장일 수 있음, 위→아래 이어짐):\n{listing}\n\n"
            f"위 이미지를 Read로 모두 연 뒤, 문제 전체를 **충실히 전사**하라 — 발문·조건·수식·풀이박스·"
            f"빈칸 (가)(나)(다)·보기 ①~⑤·배점까지 이미지 그대로. 수식은 읽기 쉬운 선형 표기(√, ², 분수 a/b)로. "
            f"한 줄로 이어 써라(줄바꿈 없이). 머리말·설명 없이 **전사 텍스트만** 출력.")


def regen_one(item):
    path, stem = item
    img = IMGDIR / (stem + '.png')
    if not img.exists():
        return dict(stem=stem, ok=False, err='no-img', cost=0.0)
    real = img.resolve()
    tiles = [str(t) for t in tile_for_vision(real)]
    args = ['claude', '-p', '--model', MODEL, '--effort', 'medium', '--allowedTools', 'Read',
            '--add-dir', str(real.parent), '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '12', '--system-prompt', SYSTEM, '--output-format', 'json', '--', prompt_for(tiles)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TO, cwd=_CLEAN_DIR, env=_CLAUDE_ENV)
        env = json.loads(r.stdout)
    except Exception:
        return dict(stem=stem, ok=False, err='timeout/err', cost=0.0)
    cost = env.get('total_cost_usd', 0) or 0.0
    if env.get('is_error') or env.get('api_error_status'):       # 401 등 에러를 텍스트로 쓰지 않기
        return dict(stem=stem, ok=False, err=f"api-error:{env.get('api_error_status', '')}", cost=cost)
    txt = (env.get('result', '') or '').strip()
    txt = re.sub(r'^```\w*\n?|\n?```$', '', txt).strip()
    txt = re.sub(r'\s+', ' ', txt)
    if len(txt) < 12:                                # 짧은 정상문제(예: "10cos(5/3π)의 값을…") 허용
        return dict(stem=stem, ok=False, err='too-short', cost=cost)
    t = path.read_text(encoding='utf-8')
    newblock = f"searchable_text: |\n  {txt}\n"
    # 블록형(| 또는 >) 교체
    t2, n = re.subn(r'(?ms)^searchable_text: [|>][-+]?\n(?: +[^\n]*\n)+', lambda m: newblock, t, count=1)
    if n != 1:                                       # 인라인/빈값형(searchable_text: '' 등) → 블록 삽입
        t2, n = re.subn(r'(?m)^searchable_text:.*\n', lambda m: newblock, t, count=1)
    if n != 1:
        return dict(stem=stem, ok=False, err='no-block', cost=cost)
    path.write_text(t2, encoding='utf-8')
    return dict(stem=stem, ok=True, err=None, cost=cost, chars=len(txt))


def targets():
    out = []
    for f in sorted(glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)):
        if 'README' in f:
            continue
        st = extract(Path(f).read_text(encoding='utf-8'))
        if '(가)' in st and '(다)' in st:
            out.append((Path(f), Path(f).stem))
    return out


def main():
    tg = targets()
    if LIMIT:
        tg = tg[:LIMIT]
    print(f"═══ 빈칸추론형 searchable_text 재생성 ({MODEL}) — {len(tg)}개 ═══\n", flush=True)
    res, tot = [], 0.0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(regen_one, it): it for it in tg}):
            r = fut.result(); res.append(r); tot += r['cost']
            mark = '✅' if r['ok'] else f"⚠ {r['err']}"
            print(f"  [{len(res)}/{len(tg)}] {r['stem']:34s} {mark}  ${r['cost']:.3f}", flush=True)
    ok = sum(r['ok'] for r in res)
    print(f"\n═══ 완료 ═══ 재생성 {ok}/{len(res)} · ${tot:.2f}", flush=True)


if __name__ == '__main__':
    main()
