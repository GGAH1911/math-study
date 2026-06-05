#!/usr/bin/env python3
"""시범 풀빌드 — 한 회차를 *처음부터* build_solution_cache로 빌드
(text-first → 이미지 사다리 Haiku→Sonnet→Opus → 검증기 → 캐시) → 기존과 비교 →
**새 빌드가 더 나으면(검증 통과 + 더 낮은 모델) 실데이터 교체, 아니면 원본 유지(회귀0).**
비파괴: 빌드는 /tmp에서, 검증기도 임시폴더. 실 md/db는 '더 나을 때만' 갱신.
환경: ROUND(2027/6월모평), TFB_WORKERS(6). SOLVE_TIMEOUT은 launch에서."""
from __future__ import annotations
import sys, re, os, shutil
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B   # noqa: E402

ROUND = os.environ.get('ROUND', '2027/6월모평')
WORKERS = int(os.environ.get('TFB_WORKERS', '6'))
TMP = Path('/tmp/trial_build'); TMP.mkdir(parents=True, exist_ok=True)
TMPVER = TMP / 'verifiers'; TMPVER.mkdir(exist_ok=True)
B.VERIFIER_DIR = TMPVER          # 검증기 임시폴더 → 실 db/solutions 보호
TIER = {'haiku': 0, 'sonnet': 1, 'opus': 2}


def solved_by(t):
    m = re.search(r'^\s*solved_by:\s*(\w+)', t, re.M)
    return m.group(1) if m else None


def tier(sb):
    return TIER.get(sb, 3)


def trial(real_md):
    t = real_md.read_text(encoding='utf-8')
    old = solved_by(t)
    t2 = re.sub(r'(?ms)^solution:.*?(?=^---)', '', t)        # un-cache → /tmp
    tmp = TMP / real_md.name; tmp.write_text(t2, encoding='utf-8')
    r = B.build_one(tmp)                                      # 풀 파이프라인 (text-first→Opus)
    new = solved_by(tmp.read_text(encoding='utf-8'))
    better = r.startswith('CACHED') and tier(new) < tier(old)  # 검증된 + 더 낮은 모델 = 더 나음
    if better:                                                # 더 나을 때만 실데이터 교체
        shutil.copy(tmp, real_md)
        v = TMPVER / (real_md.stem + '.py')
        if v.exists():
            shutil.copy(v, ROOT / 'db' / 'solutions' / (real_md.stem + '.py'))
    return dict(stem=real_md.stem, r=r, old=old, new=new, upd=better)


def main():
    files = [f for f in sorted((ROOT / 'docs' / 'problems' / ROUND).glob('*.md')) if 'README' not in f.name]
    print(f"═══ 시범 풀빌드: {ROUND} — {len(files)}문제 (처음부터 text-first→Opus→검증기) ═══\n", flush=True)
    res = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(trial, f): f for f in files}):
            d = fut.result(); res.append(d)
            mark = '⬆ UPDATED' if d['upd'] else 'kept-old'
            print(f"  [{len(res)}/{len(files)}] {d['stem']:30s} {d['r']:11s} old={d['old']} new={d['new']}  {mark}", flush=True)
    by_r = Counter(d['r'].split('(')[0] for d in res)
    cached = sum(1 for d in res if d['r'].startswith('CACHED'))
    upd = sum(d['upd'] for d in res)
    tf = sum(1 for d in res if d['r'] == 'CACHED@T')
    opus = sum(1 for d in res if d['new'] == 'opus')
    flag = sum(1 for d in res if not d['r'].startswith('CACHED'))
    print(f"\n═══ 파이프라인 검증 ═══", flush=True)
    print(f"  캐시 생성: {cached}/{len(res)} ({100*cached//len(res)}%) · 빌드실패 {flag} · 결과 {dict(by_r)}", flush=True)
    print(f"  text-first(CACHED@T) {tf} · Opus까지 에스컬레이션 {opus}", flush=True)
    print(f"  ⬆ 갱신(새 빌드가 더 나음=더 낮은 모델) {upd} · 유지(원본 보존) {len(res)-upd}", flush=True)
    print(f"  → 4단계(text-first·폴백·Opus·검증기) 전부 한 흐름에 도는지 확인 + 회귀0(더 나을 때만 교체)", flush=True)


if __name__ == '__main__':
    main()
