#!/usr/bin/env python3
"""2021 고3 교육청 4·7·10월 일괄 — 스테이징 → ingest_gyo3 → build_solution_cache.
각 월 순차(API 부하 위해). MATHSTUDY_ROOT는 launch에서 설정(워크트리)."""
import sys, os, glob, unicodedata, shutil, subprocess
from pathlib import Path

ROOT = Path(os.environ['MATHSTUDY_ROOT']).resolve()
SCRIPTS = ROOT / 'scripts'
VENV = '/home/insung/Projects/math-study/.venv/bin/python'
SRC = glob.glob('/home/insung/Downloads/taildrop/*.pdf')
MONTHS = [('4월', '4월'), ('7월', '7월'), ('10월', '10원')]   # (세션라벨, 파일검색어)
SUBJ_FK = [('미적분', '미적'), ('기하', '기하'), ('확률과통계', '확통')]


def norm(s): return unicodedata.normalize('NFC', s)


def find(terms, exclude=None):
    for f in SRC:
        n = norm(Path(f).name)
        if all(norm(t) in n for t in terms) and (not exclude or norm(exclude) not in n):
            return f
    return None


def stage(session, fterm):
    slug = f'2021_고3_{session}모의고사'
    dst = ROOT / 'db' / 'raw' / slug
    dst.mkdir(parents=True, exist_ok=True)
    for subj, fk in SUBJ_FK:
        p = find([fterm, fk], exclude='해설')
        h = find([fterm, fk, '해설'])
        if not p or not h:
            print(f"  ⚠ {session} {subj}: PDF 못찾음", flush=True)
            continue
        shutil.copy(p, dst / f'{subj}_문제.pdf')
        shutil.copy(h, dst / f'{subj}_해설.pdf')
    return slug


def run(cmd, env_extra=None):
    return subprocess.run(cmd, env={**os.environ, **(env_extra or {})}, check=False).returncode


for session, fterm in MONTHS:
    print(f"\n{'#' * 60}\n# 2021 고3 {session}\n{'#' * 60}", flush=True)
    slug = stage(session, fterm)
    print(f"  staged: {slug}", flush=True)
    rc = run([VENV, str(SCRIPTS / 'ingest_kice' / 'ingest_gyo3.py'),
              '--year', '2021', '--session', session], {'META_WORKERS': '20'})
    if rc != 0:   # 안전장치(선택 답 동일 등) 발동 → 캐시 건너뛰고 전체 중단
        print(f"  🔴 {session} 인제스트 실패(안전장치 발동 가능성) — 캐시 건너뜀, 일괄 중단", flush=True)
        raise SystemExit(f"{session} ingest failed (rc={rc})")
    mds = glob.glob(str(ROOT / 'docs' / 'problems' / '2021' / f'고3_{session}모의고사' / '*.md'))
    slugs = ','.join(Path(m).stem for m in mds)
    print(f"  풀이캐시 대상 {len(mds)}문제", flush=True)
    if slugs:
        run([VENV, str(SCRIPTS / 'build_solution_cache.py'),
             '--list', slugs, '--parallel', '20'],
            {'SOLVE_TIMEOUT': '600', 'VERIFY_RETRIES': '2'})
    print(f"  ✓ {session} 완료 (인제스트 + 풀이캐시)", flush=True)

print(f"\n{'=' * 60}\n4·7·10월 일괄 완료\n{'=' * 60}", flush=True)
