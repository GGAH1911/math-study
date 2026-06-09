#!/usr/bin/env python3
"""범용 인제스트 디스패처 — taildrop 파일명으로 회차 자동분류 → 엄격 스테이징 → 백엔드 라우팅.

매번 회차별로 어댑터+애드혹 스테이징을 새로 짜던 걸 한 곳으로 통합한다. 핵심:
  1) **자동 분류** — 파일명 정규식 RULES 로 (year, exam_type, session, grade, track/subject, role,
     answer_source, backend) 감지. 비-시험 파일(잡지·뉴스·이미지)은 조용히 무시.
  2) **엄격 스테이징** — 정확 NFC 매칭으로 db/raw/<slug>/ 에 정식 이름 배치. 회차 disambiguation
     내장(연도+회차+트랙) → 2026 가형이 2021 6월모평에 섞이는 류의 교차오염 차단.
  3) **백엔드 라우팅** — 감지 유형별로 ingest_v2 / ingest_ganah / ingest_gyo12 호출.
  4) **일괄 캐시·동기화** — 새 회차 전부 인제스트 후 풀이캐시(--parallel) + post_ingest_sync 한 번.

기본은 **dry-run**(계획만 출력, 디스크 안 건드림). 실제 실행은 --run.
이미 인제스트된 회차(docs/problems/<year>/<round_dir> 존재)는 자동 스킵(--force 로 재실행).

사용:
  python ingest_auto.py                      # taildrop 스캔 → 감지 계획 출력(dry-run)
  python ingest_auto.py --run                # 새 회차 전부 스테이징+인제스트+캐시+동기화
  python ingest_auto.py --run --only 2021_6월모평   # 특정 slug만
  python ingest_auto.py --run --no-cache --no-sync  # 인제스트만
"""
from __future__ import annotations
import os, re, sys, shutil, subprocess, unicodedata, argparse, glob
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_v2 as IV          # noqa: E402

ROOT = IV.ROOT
TAILDROP = Path(os.path.expanduser('~/Downloads/taildrop'))
PY = sys.executable
SELECTIVE = {'기하': '기하', '미적': '미적분', '확통': '확률과통계'}


def _nfc(s: str) -> str:
    return unicodedata.normalize('NFC', s)


# ── 분류 규칙 ───────────────────────────────────────────────────────────────
# 각 룰: (정규식, fn(match) -> dict). dict 필드:
#   exam_type, year, session?, grade?, agency, backend('v2'|'ganah'|'gyo12'),
#   role('문제'|'해설'|'정답'|'통합본'), track?(가형/나형), subject?(선택과목), single?
def _rules():
    R = []
    A = R.append
    # 교육청 고3 과목별 (기하/미적/확통) 문제·해설 — '10원'=10월 오타 허용
    A((re.compile(r'^(\d{4})\s+고3\s+(\d+)[월원]\s+(기하|미적|확통)(\s*해설)?\.pdf$'),
       lambda m: dict(exam_type='모의고사', year=int(m[1]), session=f'{m[2]}월', grade='고3',
                      agency='교육청', backend='v2_haesol', subject=SELECTIVE[m[3]],
                      role='해설' if m[4] else '문제')))
    # 교육청 고3 통합본 (수학 (통합본)/(정답)) — 연도 없으면 ambiguous
    A((re.compile(r'^(\d{4})?\s*고3\s+(\d+)월\s+수학\s*\((통합본|정답)\)\.pdf$'),
       lambda m: dict(exam_type='모의고사', year=int(m[1]) if m[1] else None, session=f'{m[2]}월',
                      grade='고3', agency='교육청', backend='v2',
                      role='문제' if m[3] == '통합본' else '정답')))
    # 교육청 고1/고2 단일 (해설답): "2021 고1 3월 [해설].pdf"
    A((re.compile(r'^(\d{4})\s+(고[12])\s+(\d+)월(\s*해설)?\.pdf$'),
       lambda m: dict(exam_type='모의고사', year=int(m[1]), session=f'{m[3]}월', grade=m[2],
                      agency='교육청', backend='gyo12', role='해설' if m[4] else '문제')))
    # 교육청 고1/고2 (2026 표기): "2026년-6월-고1-모의고사-수학-(문제|해설).pdf"
    A((re.compile(r'^(\d{4})년-(\d+)월-(고[12])-모의고사-수학-(문제|해설)\.pdf$'),
       lambda m: dict(exam_type='모의고사', year=int(m[1]), session=f'{m[2]}월', grade=m[3],
                      agency='교육청', backend='gyo12', role=m[4])))
    # 평가원 모평 가/나형: "2021학년도 6월 가형 [정답].pdf"
    A((re.compile(r'^(\d{4})학년도\s+(\d+)월\s+(가형|나형)(\s*정답)?\.pdf$'),
       lambda m: dict(exam_type='모의평가', year=int(m[1]), session=f'{m[2]}월', agency='평가원',
                      backend='ganah', track=m[3], role='정답' if m[4] else '문제')))
    # 평가원 수능 가/나형: "2021학년도 수능 [가형|나형] [정답].(pdf|zip)"
    A((re.compile(r'^(\d{4})학년도\s+수능(?:\s+(가형|나형))?(\s*정답)?\.(?:pdf|zip)$'),
       lambda m: dict(exam_type='수능', year=int(m[1]), agency='평가원', backend='ganah',
                      track=m[2], role='정답' if m[3] else '문제')))
    # 평가원 모평 공통선택: "2027 학년도 6월 모평 [정답표].pdf"
    A((re.compile(r'^(\d{4})\s*학년도\s+(\d+)월\s+모평(\s*정답표)?\.pdf$'),
       lambda m: dict(exam_type='모의평가', year=int(m[1]), session=f'{m[2]}월', agency='평가원',
                      backend='v2', role='정답' if m[3] else '문제')))
    # 평가원 예시 (통합형): "2028 평가원 예시문제 [정답표].pdf"
    A((re.compile(r'^(\d{4})\s+평가원\s+예시문제\s*(정답표)?\.pdf$'),
       lambda m: dict(exam_type='예시', year=int(m[1]), agency='평가원', backend='v2', single=True,
                      role='정답' if m[2] else '문제')))
    return R


RULES = _rules()


def _slug(spec: dict):
    """spec → (slug, round_dir). ganah 가/나형은 ingest_ganah 가 트랙을 안에서 처리."""
    et = spec['exam_type']
    et_norm = '모의평가' if et in ('모의평가', '모평') else et
    slug = IV.slugify_round(spec.get('year') or 0, et_norm, spec.get('session'), spec.get('grade'))
    return slug


def classify(files):
    """파일 리스트 → (rounds{slug: {meta, files:[(name,spec)]}}, unrecognized[], ambiguous[])."""
    rounds, unrec, ambig = {}, [], []
    for f in sorted(files):
        nf = _nfc(f)
        if not nf.lower().endswith(('.pdf', '.zip')):
            continue                                    # 비-PDF는 조용히 무시
        spec = None
        for rx, fn in RULES:
            m = rx.match(nf)
            if m:
                spec = fn(m)
                break
        if not spec:
            if re.search(r'고[123]|학년도|모평|평가원|예시', nf):  # 시험 같은데 미인식 → 보고
                unrec.append(nf)
            continue
        if not spec.get('year'):
            ambig.append((nf, '연도 불명')); continue
        slug = _slug(spec)
        r = rounds.setdefault(slug, {'slug': slug, 'meta': spec, 'files': []})
        r['files'].append((nf, spec))
    return rounds, unrec, ambig


def _ingested(slug: str, meta: dict) -> bool:
    year = meta.get('year')
    rd = slug.split('_', 1)[1] if '_' in slug else slug
    return bool(glob.glob(str(ROOT / 'docs' / 'problems' / str(year) / rd / '*.md')))


def _stage(slug, meta, files, d: Path):
    """감지된 파일을 db/raw/<slug>/ 에 정식 이름으로 배치 (정확 매칭)."""
    dst = ROOT / 'db' / 'raw' / slug
    dst.mkdir(parents=True, exist_ok=True)
    backend = meta['backend']
    for nf, spec in files:
        # zip 가드는 target 이름이 아니라 **소스 확장자**로 검사해야 한다.
        # ganah 트랙 케이스(가형_문제.pdf 등)는 target 이 .pdf 라 target 검사로는
        # zip 이 안 걸리고 fitz 가 zip 을 PDF 로 열다 실패한다. zip 은 사용자가 미리 풀어야.
        if nf.lower().endswith('.zip'):
            continue
        src = d / next(x for x in os.listdir(d) if _nfc(x) == nf)
        role = spec.get('role')
        if backend == 'ganah':
            trk = spec.get('track')
            if spec['exam_type'] == '수능' and not trk:        # 수능 통합 정답.pdf / zip
                name = '정답.pdf' if role == '정답' else nf      # zip 은 별도 처리 필요
            else:
                name = f'{trk}_정답.pdf' if role == '정답' else f'{trk}_문제.pdf'
        elif backend == 'gyo12':
            name = '해설.pdf' if role == '해설' else '문제.pdf'
        elif backend == 'v2_haesol':                          # 교육청 고3 과목별
            subj = spec.get('subject')
            name = f'해설_{subj}.pdf' if role == '해설' else f'{subj}_문제.pdf'
        else:                                                 # v2 (정답.pdf 기반)
            name = '정답.pdf' if role in ('정답',) else '문제.pdf'
        if name.endswith('.zip'):
            continue                                          # zip 은 사용자가 미리 풀어야
        shutil.copy2(src, dst / name)


def _dispatch(slug, meta, parallel, no_sync):
    """백엔드 어댑터 호출 (인제스트만; 캐시·동기화는 상위에서 일괄)."""
    backend = meta['backend']
    env = {**os.environ, 'MATHSTUDY_ROOT': str(ROOT)}
    y = str(meta['year'])
    if backend == 'ganah':
        et = '모평' if meta['exam_type'] in ('모의평가', '모평') else meta['exam_type']
        cmd = [PY, 'scripts/ingest_kice/ingest_ganah.py', '--year', y, '--exam-type', et, '--no-sync']
        if meta.get('session'):
            cmd += ['--session', meta['session']]
    elif backend == 'gyo12':
        cmd = [PY, 'scripts/ingest_kice/ingest_gyo12.py', '--year', y,
               '--rounds', f"{meta['grade']}_{meta['session']}", '--no-sync']
    else:  # v2 / v2_haesol
        cmd = [PY, 'scripts/ingest_kice/ingest_v2.py', '--year', y, '--exam-type', meta['exam_type']]
        if meta.get('session'):
            cmd += ['--session', meta['session']]
        if meta.get('grade'):
            cmd += ['--grade', meta['grade']]
        if meta.get('agency'):
            cmd += ['--agency', meta['agency']]
        if meta.get('single'):
            cmd += ['--single']
    return subprocess.run(cmd, env=env).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=str(TAILDROP), help='스캔 디렉토리 (기본 taildrop)')
    ap.add_argument('--run', action='store_true', help='실제 실행 (없으면 dry-run 계획만)')
    ap.add_argument('--only', default=None, help='이 slug 만')
    ap.add_argument('--force', action='store_true', help='이미 인제스트된 회차도 재실행')
    ap.add_argument('--parallel', type=int, default=20)
    ap.add_argument('--no-cache', action='store_true')
    ap.add_argument('--no-sync', action='store_true')
    a = ap.parse_args()

    d = Path(a.dir)
    rounds, unrec, ambig = classify(os.listdir(d))
    todo = []
    print(f'══════ 감지 결과 ({d}) ══════')
    for slug in sorted(rounds):
        r = rounds[slug]; meta = r['meta']
        done = _ingested(slug, meta)
        skip = done and not a.force
        tag = '✅이미적재' if done else '🆕신규'
        sub = '' if skip else ('  → 적재대상' if (not a.only or a.only == slug) else '  (--only 제외)')
        nfiles = len(r['files'])
        print(f'  {tag} {slug:22} [{meta["backend"]:9}] {nfiles}파일{sub}')
        if not skip and (not a.only or a.only == slug):
            if meta['backend'] == 'v2_haesol':            # 교육청 고3 과목별 해설 — 스테이징 미검증
                print('       ↑ 교육청 고3 과목별 해설은 디스패처 자동적재 미지원(수동) — 제외')
            else:
                todo.append(slug)
    if ambig:
        print('  ⚠ 연도불명(수동 필요):')
        for nf, why in ambig: print(f'     - {nf}  ({why})')
    if unrec:
        print('  ⚠ 시험같은데 미인식(룰 추가 필요):')
        for nf in unrec: print(f'     - {nf}')

    if not a.run:
        print(f'\n[dry-run] 적재 대상 {len(todo)}개: {todo}\n실행하려면 --run')
        return
    if not todo:
        print('\n적재할 신규 회차 없음.'); return

    print(f'\n══════ 적재 시작 {len(todo)}회차 ══════')
    ok = []
    for slug in todo:
        r = rounds[slug]
        print(f'\n── {slug} 스테이징+인제스트 ──', flush=True)
        _stage(slug, r['meta'], r['files'], d)
        if _dispatch(slug, r['meta'], a.parallel, a.no_sync):
            ok.append(slug)
        else:
            print(f'  ✗ {slug} 인제스트 실패')

    if ok:
        slugs = []
        for slug in ok:
            rd = slug.split('_', 1)[1]
            year = rounds[slug]['meta']['year']
            slugs += sorted(Path(p).stem for p in glob.glob(str(ROOT / 'docs' / 'problems' / str(year) / rd / '*.md')))
        print(f'\n══════ 텍스트 품질 게이트 {len(slugs)}문제 ══════', flush=True)
        subprocess.run([PY, 'scripts/text_quality_gate.py', '--list', ','.join(slugs)],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})   # 손상 자동 재전사 (캐시 전)
        subprocess.run([PY, 'scripts/consistency_gate.py', '--list', ','.join(slugs), '--fix'],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})   # format 오분류 자동교정
        if not a.no_cache:
            print(f'\n══════ 풀이캐시 {len(slugs)}문제 --parallel {a.parallel} ══════', flush=True)
            subprocess.run([PY, 'scripts/build_solution_cache.py', '--list', ','.join(slugs),
                            '--parallel', str(a.parallel)], env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
    if ok and not a.no_sync:
        print('\n══════ 후처리 동기화 ══════', flush=True)
        subprocess.run([PY, 'scripts/post_ingest_sync.py'], env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
    print(f'\n✓ 완료: {len(ok)}/{len(todo)}회차')


if __name__ == '__main__':
    main()
