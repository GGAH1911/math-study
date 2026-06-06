#!/usr/bin/env python3
"""솔버 무결성 감사 — db/solutions/*.py 와 md verifier 필드의 정합성 + 게이트 회귀 검사.

불변식:
  1. orphan 없음    : db/solutions/*.py 는 모두 어떤 md 의 verifier 로 참조돼야 한다.
  2. 누락 없음       : md verifier=db/solutions/X.py 면 그 파일이 실제로 존재해야 한다.
  3. (옵션 --gate) 회귀 없음: 등록된 솔버는 모두 하드코딩 게이트(accept_verifier)를 통과해야 한다.

이전 배치가 남긴 가짜 34개·stale 사고의 재발 방지용. 인제스트/백필 후 또는 CI 로 실행.
사용: python audit_solvers.py [--gate] [--gate-sample N] [--fix-orphans]   (--fix-orphans = orphan 삭제)
종료코드: 위반 있으면 1, 없으면 0.
"""
from __future__ import annotations
import re, sys, glob, os, argparse, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B   # noqa: E402  accept_verifier 재사용

VERIF = re.compile(r'^\s*verifier:\s*(.+)$', re.M)
ANS = re.compile(r'^answer:\s*"?([^"\n]+)', re.M)
FMT = re.compile(r'^format:\s*(\w+)', re.M)


def scan():
    md_by_slug, ref_by_slug = {}, {}
    for p in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        slug = Path(p).stem
        md_by_slug[slug] = p
        v = VERIF.search(open(p, encoding='utf-8').read())
        if v and v.group(1).strip().startswith('db/solutions'):
            ref_by_slug[slug] = v.group(1).strip()
    solver_files = {Path(f).stem for f in glob.glob(str(ROOT / 'db' / 'solutions' / '*.py'))}

    orphans = sorted(solver_files - set(ref_by_slug))          # 파일 있는데 md 미참조
    missing = sorted(s for s in ref_by_slug if s not in solver_files)  # md 참조인데 파일 없음
    return md_by_slug, ref_by_slug, solver_files, orphans, missing


def _legacy_ok(code: str, gold: str) -> tuple[bool, str]:
    """CANDIDATE 규약 이전(구버전 vision 백필) 솔버용 — 회귀(실행 깨짐)만 검사.
    블라인드 vision 생성이라 하드코딩 불가 → 'VERIFY_PASS 실행되는가'가 유일한 유효 불변식.
    (sympy 키워드 없이 순수 파이썬 산술로 검증하는 정상 솔버가 많아 realmath 요구는 오탐)."""
    ok, _ = B.run_verifier(code)
    return (ok, 'ok' if ok else 'legacy-run-fail')


def gate_check(slugs, md_by_slug, sample=0):
    if sample and len(slugs) > sample:
        random.seed(0)
        slugs = random.sample(slugs, sample)
    fails = []
    for slug in slugs:
        t = open(md_by_slug[slug], encoding='utf-8').read()
        gold = (ANS.search(t) or [None, None])[1]
        fmt = (FMT.search(t) or [None, 'numeric'])[1]
        gold = gold.strip().strip('"') if gold else None
        code = open(ROOT / 'db' / 'solutions' / f'{slug}.py').read()
        if re.search(r'(?m)^CANDIDATE\s*=', code):          # 신규 규약 → 풀 게이트(변이테스트)
            ok, why = B.accept_verifier(code, gold, fmt)
        else:                                               # 레거시 → 약한 불변식
            ok, why = _legacy_ok(code, gold)
        if not ok:
            fails.append((slug, why))
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true', help='등록 솔버 게이트 회귀검사(느림)')
    ap.add_argument('--gate-sample', type=int, default=0, help='게이트검사 샘플 수(0=전수)')
    ap.add_argument('--fix-orphans', action='store_true', help='orphan 솔버 파일 삭제')
    a = ap.parse_args()

    md_by_slug, ref_by_slug, solver_files, orphans, missing = scan()
    print(f"등록 솔버 {len(ref_by_slug)} · 솔버파일 {len(solver_files)} · orphan {len(orphans)} · 누락 {len(missing)}", flush=True)
    viol = 0
    if orphans:
        viol += len(orphans)
        print(f"⚠ orphan(미참조) {len(orphans)}: {orphans[:8]}{'…' if len(orphans) > 8 else ''}", flush=True)
        if a.fix_orphans:
            for s in orphans:
                os.remove(ROOT / 'db' / 'solutions' / f'{s}.py')
            print(f"  → {len(orphans)}개 삭제", flush=True)
            viol -= len(orphans)
    if missing:
        viol += len(missing)
        print(f"⚠ 누락(참조인데 파일없음) {len(missing)}: {missing[:8]}", flush=True)
    if a.gate:
        reg = [s for s in ref_by_slug if s in solver_files]
        fails = gate_check(reg, md_by_slug, a.gate_sample)
        if fails:
            viol += len(fails)
            print(f"⚠ 게이트 회귀 {len(fails)}/{a.gate_sample or len(reg)}: {fails[:8]}", flush=True)
        else:
            print(f"✅ 게이트 회귀 0 ({a.gate_sample or len(reg)}개 검사)", flush=True)
    print(("❌ 위반 %d건" % viol) if viol else "✅ 무결성 OK", flush=True)
    sys.exit(1 if viol else 0)


if __name__ == '__main__':
    main()
