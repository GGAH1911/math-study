#!/usr/bin/env python3
"""시범 인제스트-청소 — 한 회차의 결함(⋄·짧음) 문제에 gated-cleanup(recover) 적용.
인제스트 통합을 미리 검증: 결함 탐지($0) → recover(원본 pass@K → regenerate → 검증 게이트).
회귀 검증 내장(canary): text_ok 안 붙은 결함수 전후 비교 → 증가하면 회귀 경보.
환경: ROUND(2027/6월모평), TR_WORKERS(8), TR_K(3). SOLVE_TIMEOUT은 launch에서."""
from __future__ import annotations
import sys, re, glob, os
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import recover_text_defects as R   # noqa: E402  (recover, transcribe, solve_passk, overwrite_text, relabel_md)
import build_solution_cache as B   # noqa: E402

CORRUPT = re.compile(r'[⋄�□◇]')
ROUND = os.environ.get('ROUND', '2027/6월모평')
WORKERS = int(os.environ.get('TR_WORKERS', '8'))
R.K = int(os.environ.get('TR_K', '3'))


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(ans=g('answer'), fmt=g('format'))


def is_defect(st):
    return bool(CORRUPT.search(st)) or (0 < len(st) < 120)


def round_files():
    return [f for f in sorted(glob.glob(str(ROOT / 'docs' / 'problems' / ROUND / '*.md'))) if 'README' not in f]


def defect_count():
    """text_ok(검증된 것) 제외하고 남은 결함 수 = canary 기준."""
    c = 0
    for f in round_files():
        t = Path(f).read_text(encoding='utf-8')
        if re.search(r'^\s*text_ok:\s*true', t, re.M):
            continue
        if is_defect(B.extract_searchable(t)):
            c += 1
    return c


def targets():
    out = []
    for f in round_files():
        t = Path(f).read_text(encoding='utf-8')
        if re.search(r'^\s*text_ok:\s*true', t, re.M):
            continue
        st = B.extract_searchable(t); m = meta(t)
        if is_defect(st) and m['ans']:
            out.append((Path(f), m['fmt'], m['ans']))
    return out


def main():
    before = defect_count()
    tg = targets()
    print(f"═══ 시범 인제스트-청소: {ROUND} ═══", flush=True)
    print(f"  회차 {len(round_files())}문제 · 결함(⋄/짧음) {before}개 · 대상 {len(tg)}\n", flush=True)
    res = []
    TAG = {'stochastic': '✅ 원본정상(text_ok)', 'text-fixed': '✅ OCR수정', 'still-fail': '· 보존(진짜hard/도형)', 'regen-fail': '· 보존(전사실패)'}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(R.recover, it): it for it in tg}
        for fut in as_completed(futs):
            it = futs[fut]; r = fut.result(); res.append(r)
            print(f"  [{len(res)}/{len(tg)}] {it[0].stem:34s} {TAG.get(r, r)}", flush=True)
    after = defect_count()
    by = Counter(res)
    fixed = by['stochastic'] + by['text-fixed']
    print(f"\n═══ 완료 ═══ {dict(by)}", flush=True)
    print(f"  회수 {fixed} (원본정상 {by['stochastic']} · OCR수정 {by['text-fixed']}) · 보존 {by['still-fail'] + by['regen-fail']}", flush=True)
    verdict = '✅ 감소(정상)' if after <= before else '🔴 증가 = 회귀 발생!'
    print(f"  ── 회귀 검증(canary) ── 미검증 결함 {before} → {after}   {verdict}", flush=True)
    print(f"  (보존된 것은 원본 그대로 = 회귀 0. 회수된 것만 text_ok로 결함목록에서 빠짐.)", flush=True)


if __name__ == '__main__':
    main()
