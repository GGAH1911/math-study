#!/usr/bin/env python3
"""솔버 백필 — gold-match·솔버없음 문제에 **Haiku-only** 로 솔버(파라미터 재계산기) 생성.

솔버는 단순 답체크가 아니라 **유사문제 무한 재생성용 파라미터 솔버** (원식을 코드로 인코딩).
크레딧 절약 모드: **Sonnet/Opus 에스컬레이트 안 함.** Haiku 동티어 재롤(REROLL)로 솔버 코드의
확률적 버그(scipy 미설치 등은 설치로 해결됨)를 흡수. Haiku가 끝내 실패하면 **gold-match 유지
(무손상·additive)** — 절대 verified:true 를 깨지 않는다.

대상: verified:true 인데 verifier 가 db/solutions/*.py 가 아닌 것 (gold-match 단답 962 + 손풀이 등).
사용: python backfill_solvers.py [--parallel 16] [--limit N]   (REROLL 환경변수로 재롤 조정)
"""
from __future__ import annotations
import sys, os, re, glob, argparse, time
import concurrent.futures as cf
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_solution_cache as B   # noqa: E402  call_model/run_verifier/tile_for_vision/상수 재사용

REROLL = int(os.environ.get('REROLL', '2'))     # Haiku 동티어 재롤 최대(총 시도 = REROLL+1)


def targets(limit=None):
    out = []
    for p in sorted(glob.glob(str(B.ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)):
        t = open(p, encoding='utf-8').read()
        if not re.search(r'^\s*verified:\s*true', t, re.M):
            continue
        ver = re.search(r'^\s*verifier:\s*(.+)$', t, re.M)
        if ver and ver.group(1).strip().startswith('db/solutions'):
            continue                              # 이미 솔버 있음
        out.append(p)
    return out[:limit] if limit else out


def _extract_steps(md: str) -> str:
    """md 의 solution.steps 를 읽어 텍스트로 (open-book 프롬프트에 주입)."""
    m = re.search(r'(?m)^\s*steps:\s*$\n((?:\s+-\s+.*\n?)+)', md)
    if not m:
        return ''
    out = []
    for s in re.findall(r'(?m)^\s+-\s+(.*)$', m.group(1)):
        s = s.strip()
        try:
            import json as _j
            out.append(_j.loads(s))                # JSON 인코딩 문자열 디코드
        except Exception:
            out.append(s.strip('"'))
    return '\n'.join(f'- {x}' for x in out)


def backfill_one(p: str):
    slug = Path(p).stem
    t = open(p, encoding='utf-8').read()
    gm = re.search(r'^answer:\s*"?([^"\n]+)', t, re.M)
    gold = gm.group(1).strip().strip('"') if gm else None
    fmt = (re.search(r'^format:\s*(\w+)', t, re.M) or [None, 'numeric'])[1]
    if not gold:
        return slug, 'no-gold'
    problem = B.extract_searchable(t)             # searchable_text (문제 본문)
    if not problem:
        return slug, 'no-text'
    steps = _extract_steps(t)                     # 기존 검증된 풀이단계 (있으면)
    hint = ''
    for _ in range(REROLL + 1):                   # Haiku-only · open-book
        try:
            sol = B.call_openbook(problem, gold, fmt, steps, 'haiku', 'high', hint)
        except Exception:
            sol = None
        if not sol:
            continue
        vp = sol.get('verifier_python', '') or ''
        if not vp:
            continue
        good, why = B.hardcode_gate(vp, gold, fmt)  # ★ 하드코딩 게이트(변이테스트)
        if not good:
            if why == 'orig-fail':
                hint = ('⚠ 직전 검산기가 VERIFY_FAIL/크래시였다. 원래 문제의 식·조건에 CANDIDATE 를 '
                        '역대입하는 로직을 처음부터 재검토해 다시 작성하라.')
            elif why.startswith('mutation-pass'):
                hint = ('⚠ 직전 검산기가 *틀린 답*에도 VERIFY_PASS 를 냈다(하드코딩 의심). 원래 문제의 '
                        '식·조건에 CANDIDATE 를 실제로 대입/풀이해서, 틀린 값이면 반드시 VERIFY_FAIL 이 나오게 하라.')
            elif why == 'no-realmath':
                hint = ('⚠ 직전 검산기에 실제 수식 풀이(sympy solve/Eq/subs/isclose 등)가 없다. '
                        '문제의 원래 식을 코드로 표현하고 CANDIDATE 를 대입해 판정하라.')
            elif why == 'self-compare':
                hint = ('⚠ 직전 검산기가 답을 자기 자신과 직접 비교(if CANDIDATE == 정답)했다. 금지다. '
                        '원래 문제의 식에 대입한 결과로만 판정하라.')
            elif why == 'no-CANDIDATE':
                hint = '⚠ 맨 윗줄에 CANDIDATE = <정답> 정의가 없다. 반드시 그렇게 시작하라.'
            continue
        B.VERIFIER_DIR.mkdir(parents=True, exist_ok=True)
        (B.VERIFIER_DIR / f'{slug}.py').write_text(vp, encoding='utf-8')
        t2 = open(p, encoding='utf-8').read()     # 최신 재읽기(레이스 안전)
        rel = f'db/solutions/{slug}.py'
        if re.search(r'^\s*verifier:\s*.+$', t2, re.M):
            t2 = re.sub(r'(^\s*verifier:\s*).+$', rf'\g<1>{rel}', t2, count=1, flags=re.M)
        else:                                     # verifier 라인 없으면 verified 다음에 삽입
            t2 = re.sub(r'(^(\s*)verified:\s*true\s*$)', rf'\g<1>\n\g<2>verifier: {rel}', t2, count=1, flags=re.M)
        open(p, 'w', encoding='utf-8').write(t2)
        return slug, 'SOLVER'
    return slug, 'KEEP-GOLD'                       # 게이트 통과 실패 → gold-match 유지(무손상)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--parallel', type=int, default=16)
    ap.add_argument('--limit', type=int, default=None)
    a = ap.parse_args()
    tg = targets(a.limit)
    print(f"대상 {len(tg)}문제 · Haiku-only(에스컬레이트X) · 재롤{REROLL} · 병렬{a.parallel}", flush=True)
    res = Counter(); done = 0; t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as ex:
        futs = [ex.submit(backfill_one, p) for p in tg]
        for fu in cf.as_completed(futs):
            slug, r = fu.result()
            res[r] += 1; done += 1
            mark = {'SOLVER': '✅', 'KEEP-GOLD': '·'}.get(r, '⚠')
            print(f"  [{done}/{len(tg)}] {mark} {slug} → {r}", flush=True)
    print(f"\n완료 ({time.time() - t0:.0f}s): {dict(res)}", flush=True)
    print(f"  솔버 추가 {res['SOLVER']} / gold유지 {res['KEEP-GOLD']} / 스킵 {res['no-gold'] + res['no-text']}", flush=True)
