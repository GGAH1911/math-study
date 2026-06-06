#!/usr/bin/env python3
"""lite 솔버(SOLVER-LITE) → full 파라미터 솔버 승격 — 하이쿠 전용.

lite 는 '최종 관계식만' 검증해서 정답 검산은 되나 *유사문제 재생성*은 못 한다.
lite 검산기를 앵커로, 문제 계수를 키워드 인자로 노출하는 def solve(**params) 재계산기로 확장한다.
승격 게이트 = 하드코딩 게이트 + **파라미터 변이테스트**(계수를 바꾸면 답이 바뀜 = 재생성 가능).
통과 시만 full 로 교체, 실패하면 lite 유지(무손상). 하이쿠 확률성 → loop-until-promoted.

대상 탐지:
  --list slug1,slug2   특정 슬러그
  --all                db/solutions/*.py 중 '# verifier-tier: lite' 마커 가진 것
  --from-log PATH      백필 로그에서 'SOLVER-LITE' 슬러그 추출 (마커 없는 기존 lite용)
사용: python promote_lite.py --all [--rerolls 3] [--parallel 8]
"""
from __future__ import annotations
import re, sys, glob, argparse
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B   # noqa: E402

LITE_MARK = '# verifier-tier: lite'


def _md_for(slug):
    hits = glob.glob(str(ROOT / 'docs' / 'problems' / '**' / f'{slug}.md'), recursive=True)
    return hits[0] if hits else None


def _extract_steps(md_text):
    m = re.search(r'(?m)^\s*steps:\s*$\n((?:\s+-\s+.*\n?)+)', md_text)
    if not m:
        return ''
    import json as _j
    out = []
    for s in re.findall(r'(?m)^\s+-\s+(.*)$', m.group(1)):
        s = s.strip()
        try:
            out.append(_j.loads(s))
        except Exception:
            out.append(s.strip('"'))
    return '\n'.join(f'- {x}' for x in out)


def promote_one(slug, rerolls):
    sp = ROOT / 'db' / 'solutions' / f'{slug}.py'
    md = _md_for(slug)
    if not sp.exists() or not md:
        return dict(slug=slug, ok=False, why='no-file')
    lite_code = sp.read_text(encoding='utf-8')
    t = open(md, encoding='utf-8').read()
    gold = (re.search(r'^answer:\s*"?([^"\n]+)', t, re.M) or [None, None])[1]
    fmt = (re.search(r'^format:\s*(\w+)', t, re.M) or [None, 'numeric'])[1]
    gold = gold.strip().strip('"') if gold else None
    problem = B.extract_searchable(t)
    steps = _extract_steps(t)
    if not (gold and problem):
        return dict(slug=slug, ok=False, why='no-meta')

    hint = ''
    for _ in range(rerolls + 1):
        try:
            sol = B.call_promote(problem, gold, fmt, steps, lite_code, 'haiku', 'high', hint)
        except Exception:
            sol = None
        vp = (sol or {}).get('verifier_python', '') or ''
        if not vp:
            continue
        good_hc, why_hc = B.accept_verifier(vp, gold, fmt)         # 하드코딩 게이트
        if not good_hc:
            hint = f'⚠ 직전 시도가 게이트({why_hc}) 실패. CANDIDATE 를 계수에서 계산하라.'
            continue
        good_pm, why_pm = B.param_mutation_gate(vp, gold)          # 파라미터 변이테스트
        if not good_pm:
            hint = ('⚠ 직전 솔버는 계수를 바꿔도 답이 안 바뀐다(' + why_pm + '). solve(**계수) 의 '
                    '키워드 인자로부터 답을 실제로 forward 계산해, 계수가 바뀌면 답도 바뀌게 하라.')
            continue
        sp.write_text(vp, encoding='utf-8')                        # full 로 교체(마커 제거됨)
        return dict(slug=slug, ok=True, why='promoted')
    return dict(slug=slug, ok=False, why='stay-lite')


def find_targets(args):
    if args.list:
        return [s.strip() for s in args.list.split(',') if s.strip()]
    if args.from_log:
        slugs = []
        for line in open(args.from_log):
            m = re.search(r'(\S+) → SOLVER-LITE', line)
            if m:
                slugs.append(m.group(1))
        return slugs
    # --all: 마커 가진 파일
    out = []
    for f in glob.glob(str(ROOT / 'db' / 'solutions' / '*.py')):
        try:
            head = open(f, encoding='utf-8').read(60)
        except Exception:
            continue
        if LITE_MARK in head:
            out.append(Path(f).stem)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--from-log')
    ap.add_argument('--rerolls', type=int, default=3)
    ap.add_argument('--parallel', type=int, default=8)
    a = ap.parse_args()
    targets = find_targets(a)
    print(f"═══ lite→full 승격 — {len(targets)}개 (재롤{a.rerolls}·병렬{a.parallel}) ═══", flush=True)
    res = []
    with ThreadPoolExecutor(max_workers=a.parallel) as ex:
        for fut in as_completed({ex.submit(promote_one, s, a.rerolls): s for s in targets}):
            r = fut.result()
            res.append(r)
            mark = '✅승격' if r['ok'] else f"· {r['why']}"
            print(f"  [{len(res)}/{len(targets)}] {r['slug']} → {mark}", flush=True)
    c = Counter(r['why'] for r in res)
    print(f"\n═══ 완료 ═══ 승격 {sum(r['ok'] for r in res)}/{len(res)} · {dict(c)}", flush=True)


if __name__ == '__main__':
    main()
