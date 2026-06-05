#!/usr/bin/env python3
"""retry-on-FLAG 검증 — 직전 풀빌드서 FLAG였던 3문제를 *새 재시도 로직*으로 재빌드.
비파괴: /tmp에서 빌드 + 검증기도 임시폴더. 실 md/db 안 건드림.
CACHED로 바뀌면 = 검증기-코딩 실패(forbidden/crash/VERIFY_FAIL)를 같은 모델 재시도가 흡수한 것.
환경: VERIFY_RETRIES(2), SOLVE_TIMEOUT(launch에서)."""
from __future__ import annotations
import sys, re, glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B   # noqa: E402

TMP = Path('/tmp/retry_test'); TMP.mkdir(parents=True, exist_ok=True)
TMPVER = TMP / 'verifiers'; TMPVER.mkdir(exist_ok=True)
B.VERIFIER_DIR = TMPVER            # 검증기 임시폴더 → 실 db/solutions 보호

PREV = {
    '2027_6월모평_공통_04':   'FLAG(opus:verify-fail:forbidden-import)',
    '2027_6월모평_미적분_28':  'FLAG(opus:verify-fail:Traceback)',
    '2027_6월모평_공통_15':   'FLAG(opus:verify-fail:VERIFY_FAIL)',
}


def find_md(stem):
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '2027' / '**' / '*.md'), recursive=True):
        if Path(f).stem == stem:
            return Path(f)
    return None


def rebuild(stem):
    md = find_md(stem)
    if not md:
        return stem, 'NOT-FOUND', ''
    t = md.read_text(encoding='utf-8')
    t2 = re.sub(r'(?ms)^solution:.*?(?=^---)', '', t)        # un-cache → /tmp
    tmp = TMP / md.name; tmp.write_text(t2, encoding='utf-8')
    r = B.build_one(tmp)
    bt = tmp.read_text(encoding='utf-8')
    esc = re.search(r'(?ms)^\s*escalation:\s*\n(.*?)(?=^\s*\w+:\s|\Z)', bt)
    return stem, r, (re.sub(r'\s+', ' ', esc.group(1)).strip()[:220] if esc else '')


def main():
    print(f"═══ retry-on-FLAG 검증 — 직전 FLAG 3문제 재빌드 (VERIFY_RETRIES={B.VERIFY_RETRIES}) ═══\n", flush=True)
    recovered = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(rebuild, s): s for s in PREV}
        done = 0
        for fut in as_completed(futs):
            stem, r, esc = fut.result(); done += 1
            ok = r.startswith('CACHED')
            recovered += ok
            verdict = '🟢 회복(CACHED)' if ok else '🔴 여전히 FLAG'
            print(f"  [{done}/3] {stem}", flush=True)
            print(f"        이전: {PREV.get(stem)}", flush=True)
            print(f"        이제: {r}   {verdict}", flush=True)
            if esc:
                print(f"        escalation: {esc}", flush=True)
            print(flush=True)
    print(f"═══ 끝 ═══ 회복 {recovered}/3 — CACHED면 retry-on-FLAG가 검증기-코딩 실패를 흡수한 것.", flush=True)


if __name__ == '__main__':
    main()
