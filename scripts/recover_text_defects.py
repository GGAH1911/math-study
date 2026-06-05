#!/usr/bin/env python3
"""텍스트결함 비회귀 회수 — 짧은 텍스트로 못 푼 escalated(비도형) 문제를:
1) 원본 텍스트 pass@K: 풀리면 stochastic miss → 재라벨만(텍스트 불변).
2) 안 되면 regenerate(이미지 재-OCR, 충실 전사) → 새 텍스트 pass@K:
     - 풀리면 → 새 텍스트 채택(overwrite) + 재라벨.   (검증된 개선)
     - 안 풀리면 → 원본 그대로 revert.                (회귀 0)
대상: solved_by∈{sonnet,opus} · text_ok 없음 · 비도형 · searchable_text 1~149자.
환경: RTD_K(3), RTD_WORKERS(8), RTD_LIMIT(0). 속도: SOLVE_TIMEOUT(120)을 launch에서 세팅."""
from __future__ import annotations
import re, glob, os, sys, json, subprocess
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B   # noqa: E402  (call_model_text, run_verifier, extract_searchable; TIMEOUT_S=SOLVE_TIMEOUT)
from tiling import tile_for_vision  # noqa: E402

K = int(os.environ.get('RTD_K', '3'))
WORKERS = int(os.environ.get('RTD_WORKERS', '8'))
LIMIT = int(os.environ.get('RTD_LIMIT', '0'))


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(ans=g('answer'), fmt=g('format'), sb=g('solved_by'))


def targets():
    out = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        m = meta(t)
        if m['sb'] not in ('sonnet', 'opus'):
            continue
        if re.search(r'^\s*text_ok:\s*true', t, re.M):
            continue
        if re.search(r'^has_figure:\s*true', t, re.M) or ('그림과 같이' in t):  # 도형 제외(텍스트로 못 고침)
            continue
        st = B.extract_searchable(t)
        if not (0 < len(st) < 150) or not m['ans']:
            continue
        out.append((Path(f), m['fmt'], m['ans']))
    return out


def solve_passk(text, fmt, ans):
    metastr = f"문항 형식: {'객관식 5지선다' if fmt == 'choice' else '단답형(정수 정답)'}"
    for _ in range(K):                                  # early-exit: 한 번이라도 맞으면 성공
        sol = B.call_model_text(text, fmt, metastr, 'haiku', 'high')
        if not sol or str(sol.get('answer')).strip().strip('\'"') != ans:
            continue
        if fmt == 'choice' and not B.run_verifier(sol.get('verifier_python', ''))[0]:
            continue
        return True
    return False


def transcribe(stem):
    img = (IMGDIR / (stem + '.png')).resolve()
    if not img.exists():
        return None
    tiles = [str(t) for t in tile_for_vision(img)]
    listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))
    pr = (f"문제 이미지:\n{listing}\n\n위 이미지를 Read로 열어 문제 전체를 **충실히 전사**하라 — "
          f"발문·조건·**모든 수식·방정식·점화식·함수 정의**·보기까지 이미지 그대로 (요약하거나 '주어진다'로 생략 절대 금지). "
          f"수식은 선형 표기(√, ², 분수 a/b). 한 줄로 이어 써라. 머리말 없이 전사 텍스트만.")
    args = ['claude', '-p', '--model', 'sonnet', '--effort', 'medium', '--allowedTools', 'Read', '--add-dir', str(img.parent),
            '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch', '--max-turns', '10', '--output-format', 'json', '--', pr]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=200)
        env = json.loads(r.stdout)
    except Exception:
        return None
    txt = (env.get('result', '') or '').strip()
    txt = re.sub(r'\s+', ' ', re.sub(r'^```\w*\n?|\n?```$', '', txt).strip())
    return txt if len(txt) > 12 else None   # 가드 완화: 짧은 문제(예: 단순 지수계산)도 허용. 진짜 빈출력만 거르고, 나머지는 pass@3가 검증.


def relabel_md(p):
    t = p.read_text(encoding='utf-8')
    t2, n = re.subn(r'^(\s*)solved_by:\s*\w+\s*$',
                    lambda mm: f"{mm.group(1)}solved_by: haiku\n{mm.group(1)}text_ok: true", t, count=1, flags=re.M)
    if n == 1 and 'text_ok: true' in t2:
        p.write_text(t2, encoding='utf-8')


def overwrite_text(p, newtxt):
    t = p.read_text(encoding='utf-8')
    nb = f"searchable_text: |\n  {newtxt}\n"
    t2, n = re.subn(r'(?ms)^searchable_text: \|\n(?: +[^\n]*\n)+', lambda m: nb, t, count=1)
    if n == 1:
        p.write_text(t2, encoding='utf-8')


def recover(item):
    p, fmt, ans = item
    orig = B.extract_searchable(p.read_text(encoding='utf-8'))
    if orig and solve_passk(orig, fmt, ans):           # 1) 원본 pass@K → stochastic
        relabel_md(p); return 'stochastic'
    new = transcribe(p.stem)                            # 2) regenerate
    if not new:
        return 'regen-fail'
    if solve_passk(new, fmt, ans):                     # 새 텍스트 검증 → 채택
        overwrite_text(p, new); relabel_md(p); return 'text-fixed'
    return 'still-fail'                                 # 3) 둘 다 실패 → revert(불변)


def main():
    tg = targets()
    if LIMIT:
        tg = tg[:LIMIT]
    print(f"═══ 텍스트결함 비회귀 회수 (원본 pass@{K} → regenerate → 검증 keep/revert) — {len(tg)}개 ═══", flush=True)
    print("  원본으로 풀림=stochastic(텍스트불변) · 새텍스트로 풀림=text-fixed · 둘다 실패=still-fail(revert)\n", flush=True)
    res = []
    TAG = {'stochastic': '✅ stochastic (원본·텍스트불변)', 'text-fixed': '✅ text-fixed (OCR 수정)',
           'still-fail': '· still-fail (revert·진짜 도형/hard)', 'regen-fail': '⚠ regen-fail'}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(recover, it): it for it in tg}
        for fut in as_completed(futs):
            it = futs[fut]; r = fut.result(); res.append(r)
            print(f"  [{len(res)}/{len(tg)}] {it[0].stem:34s} {TAG[r]}", flush=True)
    by = Counter(res)
    rec = by['stochastic'] + by['text-fixed']
    print(f"\n═══ 완료 ═══ 추가 회수 {rec}/{len(res)}  {dict(by)}", flush=True)
    print(f"  stochastic(재시도만으로 회수, 텍스트 멀쩡) {by['stochastic']} · text-fixed(OCR 고쳐 회수) {by['text-fixed']}", flush=True)
    print(f"  still-fail(텍스트 고쳐도 안 됨 = 진짜 도형/hard, 원본 revert) {by['still-fail']}", flush=True)


if __name__ == '__main__':
    main()
