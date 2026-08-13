#!/usr/bin/env python3
"""교육청 고1·고2 전국연합학력평가 (단일과목 30문항) — 인제스트 어댑터.

고1/고2 학평은 공통+선택이 아니라 *단일과목 30문항* 시험지다 (객관식 1-21, 단답 22-30).
정답은 별도 정답.pdf가 없고 **해설.pdf 안의 정답표**가 유일한 소스 →
`answer_textlayer.parse_haesol_single` (find_tables 격자 추출; 유니코드 ①·HyhwpEQ PUA·
CJK 글리프·평문 ASCII 단답을 모두 흡수, 회차마다 폰트/레이아웃 달라도 결정적 디코드).

데이터 모델: 회차 `2021_<고1|고2>_<N월>모의고사`, subject='단일'.
스테이징: db/raw/<slug>/{문제.pdf, 해설.pdf}
사용: python ingest_gyo12.py [--rounds 고1_3월,고2_11월,...] [--year 2021]
                             [--with-cache] [--no-sync] [--limit N] [--parallel 30]
기존 ingest_v2 헬퍼만 재사용(회귀0). MATHSTUDY_ROOT 로 워크트리 오버라이드.
"""
from __future__ import annotations
import sys, os, json, argparse, subprocess, time
from pathlib import Path
import concurrent.futures as cf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_v2 as IV          # noqa: E402  render/bbox/crop/meta/md/db 헬퍼
import answer_textlayer as AT   # noqa: E402  parse_haesol_single (해설 정답표)
from PIL import Image           # noqa: E402

ROOT = IV.ROOT
EXAM_TYPE = '모의고사'
AGENCY = '교육청'
SUBJECT = '단일'
GRADES = ['고1', '고2']
SESSIONS = ['3월', '6월', '9월', '11월']


def _fmt(n: int) -> str:
    """시험구조상 고정: 1~21 객관식, 22~30 단답형 (문제 안 보고 번호로)."""
    return 'choice' if 1 <= n <= 21 else 'numeric'


def ingest_round(year: int, grade: str, session: str, limit=None) -> dict:
    slug = IV.slugify_round(year, EXAM_TYPE, session, grade)      # 2021_고1_3월모의고사
    raw = ROOT / 'db' / 'raw' / slug
    images_dir = raw / 'images'; images_dir.mkdir(parents=True, exist_ok=True)
    prob_pdf, hae_pdf = raw / '문제.pdf', raw / '해설.pdf'
    print(f'══════ {slug} (고1/고2 단일과목 어댑터) ══════', flush=True)
    if not prob_pdf.exists() or not hae_pdf.exists():
        print(f'  ⚠ PDF 없음 (문제={prob_pdf.exists()} 해설={hae_pdf.exists()})', flush=True)
        return {'round': slug, 'ok': False}

    # 1) render + bbox(30) + subject='단일'
    pages = IV.render_pdf_pages(prob_pdf, raw / 'pages')
    page_by_num = {int(p.stem[1:]): p for p in pages}
    entries = []
    for e in IV.extract_problem_bboxes(prob_pdf, EXAM_TYPE, session):
        e['subject'] = SUBJECT                       # bbox는 '공통'으로 찍지만 단일과목이 맞다
        e['_pdf'] = prob_pdf
        e['_page_png'] = page_by_num.get(e['page_num'])
        entries.append(e)
    entries.sort(key=lambda e: e['number'])
    print(f'  ✓ bbox {len(entries)} 문제', flush=True)
    if limit:
        entries = entries[:limit]

    # 2) 크롭
    for e in entries:
        name = f'{slug}_{SUBJECT}_{e["number"]:02d}.png'
        img_path = images_dir / name
        e['image_fs'] = f'db/raw/{slug}/images/{name}'
        e['image_url'] = f'/problem-images/{name}'
        e['image_path'] = str(img_path.resolve())    # vision 폴백용
        page_im = Image.open(e['_page_png'])
        if not IV.crop_problem(page_im, e['bbox_px'], img_path, exam_type=EXAM_TYPE):
            page_im.crop(e['bbox_px']).save(img_path)     # degenerate 폴백
        IV._ensure_web_symlink(img_path)
    print(f'  ✓ 크롭 {len(entries)}장', flush=True)

    # 3) 메타데이터 (PDF텍스트+Haiku, 병렬, vision 폴백)
    units = IV.load_concept_index(); meta_cache = raw / 'meta_cache'

    def meta_one(e):
        # 메타 실패(예: claude 인증 401·타임아웃)는 *비치명적* — 빈 meta로 강등하고 계속.
        # 한 문항 실패가 240문제 오케스트레이터를 죽이면 안 된다.
        m = {}
        try:
            m = IV.extract_metadata(pdf_path=e['_pdf'], page_num=e['page_num'], bbox_pdf=e['bbox_pdf'],
                                    number=e['number'], subject=SUBJECT, units_index=units,
                                    cache_dir=meta_cache, cache_key=f'{SUBJECT}_{e["number"]:02d}', timeout=60,
                                    # ★이미지 직독 + 과목/학년/연도 스코프 — 텍스트레이어는 지수를 뭉갠다
                                    image_path=Path(e['image_path']) if e.get('image_path') else None,
                                    grade=e.get('grade'), year=e.get('year'))
            if not (isinstance(m, dict) and len((m.get('searchable_text') or '').strip()) >= 10):
                import vision_meta
                m2 = vision_meta.extract_metadata(Path(e['image_path']), units,  # Path 필수(.stem)
                                                  cache_dir=meta_cache, timeout=90)
                if m2 and (m2.get('searchable_text') or '').strip():
                    m = m2
        except Exception as ex:
            print(f'  ⚠ meta 강등 #{e["number"]:02d}: {type(ex).__name__}: {str(ex)[:80]}', flush=True)
            m = m if isinstance(m, dict) else {}
        return e, m
    nfail = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('META_WORKERS', '20'))) as ex:
        for e, m in ex.map(meta_one, entries):
            e['meta'] = m
            if not (isinstance(m, dict) and m.get('unit')):
                nfail += 1
    print(f'  ✓ 메타데이터 (unit실패 {nfail})', flush=True)

    # 4) 정답 (해설.pdf 정답표 → parse_haesol_single, find_tables 격자)
    flat = AT.parse_haesol_single(hae_pdf)           # {('단일', num): ans}
    answers = {str(n): a for (_s, n), a in flat.items()}
    if not limit:
        assert len(answers) == 30, f"🔴 {slug} 정답 {len(answers)}개 (30 아님) — 해설 정답표 파싱 점검"
    print(f'  ✓ 정답 {len(answers)}개 (해설 정답표)', flush=True)

    # 5) markdown + DB
    written = []
    for e in entries:
        num = e['number']; ans = answers.get(str(num)); meta = e.get('meta') or {}
        prob = {'subject': SUBJECT, 'number': num,
                'score': IV._guess_score(num, EXAM_TYPE, grade),
                'format': _fmt(num), 'body': '',
                'image_paths': [e['image_fs']],
                'searchable_text': meta.get('searchable_text', '')}
        us = meta.get('unit') if isinstance(meta, dict) else None
        if us:
            IV._ensure_concept_exists(us, parent_unit=None, concept_type='unit')
        for sp in (meta.get('concepts') or []) if isinstance(meta, dict) else []:
            IV._ensure_concept_exists(sp, parent_unit=us, concept_type='definition')
        IV.write_markdown_v2(prob, meta, ans, e['image_url'], e['image_fs'],
                             slug, year, EXAM_TYPE, session, grade=grade, agency=AGENCY)
        written.append({'prob': prob, 'mapping': meta, 'answer': ans})
        print(f'  [{num:>2}] ans={ans!s:>4} {_fmt(num)[:3]} {prob["score"]}점 unit={meta.get("unit","?")}', flush=True)

    IV.db_upsert(written, year, EXAM_TYPE, session,
                 f'db/raw/{slug}/문제.pdf', grade=grade, agency=AGENCY)
    print(f'  ✓ DB upsert {len(written)}문제', flush=True)
    return {'round': slug, 'ok': True, 'count': len(written)}


def _parse_rounds(spec: str):
    """'고1_3월,고2_11월' → [('고1','3월'),('고2','11월')]. 없으면 전체 8회차."""
    if not spec:
        return [(g, s) for g in GRADES for s in SESSIONS]
    out = []
    for tok in spec.split(','):
        g, s = tok.strip().split('_', 1)
        out.append((g, s))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2021)
    ap.add_argument('--rounds', default='', help='예: 고1_3월,고2_11월 (생략 시 8회차 전수)')
    ap.add_argument('--with-cache', action='store_true', help='인제스트 후 풀이 캐시까지')
    ap.add_argument('--no-sync', action='store_true', help='후처리 동기화 생략')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--parallel', type=int, default=30, help='풀이 캐시 병렬도')
    a = ap.parse_args()

    rounds = _parse_rounds(a.rounds)
    results = []
    t0 = time.time()
    for grade, session in rounds:
        rs = time.time()
        r = ingest_round(a.year, grade, session, a.limit)
        r['secs'] = round(time.time() - rs)
        results.append(r)
        print(f'  └ {r["round"]} {"✓" if r.get("ok") else "✗"} ({r["secs"]}s)\n', flush=True)
    ok = [r for r in results if r.get('ok')]
    print(f'══════ 인제스트 {len(ok)}/{len(results)} 회차, {sum(r.get("count",0) for r in ok)}문제 ({time.time()-t0:.0f}s) ══════', flush=True)
    print(json.dumps(results, ensure_ascii=False))

    if ok:
        slugs = []
        for r in ok:
            md_dir = ROOT / 'docs' / 'problems' / str(a.year) / r['round'].split('_', 1)[1]
            slugs += sorted(p.stem for p in md_dir.glob('*.md'))
        print(f'\n══════ 텍스트 품질 게이트 {len(slugs)}문제 ══════', flush=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'text_quality_gate.py'),
                        '--list', ','.join(slugs)],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})   # 손상 자동 재전사 (캐시 전)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'consistency_gate.py'),
                        '--list', ','.join(slugs), '--fix'],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})   # format 오분류 자동교정
        if a.with_cache:
            print(f'\n══════ 풀이 캐시 {len(slugs)}문제 (병렬 {a.parallel}) ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_solution_cache.py'),
                            '--list', ','.join(slugs), '--parallel', str(a.parallel)],
                           env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
    if ok and not a.no_sync:
        print('\n══════ 후처리 동기화 (역인덱스·그래프 + dev 리프레시) ══════', flush=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'post_ingest_sync.py')],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
    print('\n✓ 파이프라인 완료', flush=True)
