#!/usr/bin/env python3
"""교육청 고3 (2022포맷 공통+선택) — 멀티 선택PDF 인제스트 어댑터.

기존 회차는 단일 `문제.pdf`+`정답.pdf`지만, 2021 고3 교육청 세트는
  · 문제: 과목별 PDF 3개 (미적분/기하/확률과통계), 각 = 공통(1-22)+선택(23-30)
  · 정답: 해설 PDF 안 정답표 (정답.pdf 없음)
구조다. → 공통은 미적분PDF 한 곳에서, 각 선택은 자기 PDF에서 크롭하고,
정답은 answer_textlayer.parse_haesol_answers(결정론·비전0)로 주입.

기존 ingest_round_v2 는 *건드리지 않고* 그 헬퍼함수들만 재사용(회귀0).
스테이징: db/raw/<slug>/{미적분,기하,확률과통계}_{문제,해설}.pdf
사용: python ingest_gyo3.py --year 2021 --session 3월 [--grade 고3] [--limit N]
"""
from __future__ import annotations
import sys, os, json, argparse, subprocess
from pathlib import Path
import concurrent.futures as cf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_v2 as IV          # noqa: E402  (모든 헬퍼: render/bbox/crop/meta/md/db)
import answer_textlayer as A    # noqa: E402  (parse_haesol_answers)
from PIL import Image           # noqa: E402

ROOT = IV.ROOT
SELECTIVES = ['미적분', '기하', '확률과통계']
EXAM_TYPE = '모의고사'
AGENCY = '교육청'


def _fmt_by_num(n):
    """format은 시험 구조상 고정 — 문제를 보고 판단하지 않는다.
    공통+선택(46): 1-15 객관식, 16-22 단답 / 23-28 객관식, 29-30 단답."""
    return 'choice' if (1 <= n <= 15 or 23 <= n <= 28) else 'numeric'


def ingest(year: int, session: str, grade: str = '고3', limit: int | None = None) -> dict:
    slug = IV.slugify_round(year, EXAM_TYPE, session, grade)
    raw = ROOT / 'db' / 'raw' / slug
    images_dir = raw / 'images'; images_dir.mkdir(parents=True, exist_ok=True)
    print(f'══════ {slug} (교육청 고3 멀티선택 어댑터) ══════', flush=True)

    # 1) 과목별 PDF: 페이지 렌더 + bbox. 공통은 미적분PDF만, 선택은 각 PDF.
    entries = []
    for subj in SELECTIVES:
        pdf = raw / f'{subj}_문제.pdf'
        if not pdf.exists():
            print(f'  ⚠ 없음: {pdf.name}', flush=True); continue
        pages = IV.render_pdf_pages(pdf, raw / f'pages_{subj}')
        page_by_num = {int(p.stem[1:]): p for p in pages}
        for e in IV.extract_problem_bboxes(pdf, exam_type=EXAM_TYPE, grade=grade):
            if e['number'] <= 22:
                if subj != '미적분':
                    continue                 # 공통(1-22)은 미적분PDF 한 곳에서만
                e['subject'] = '공통'
            else:
                e['subject'] = subj          # 선택(23-30)은 파일 과목으로 확정
            e['_pdf'] = pdf
            e['_page_png'] = page_by_num.get(e['page_num'])
            entries.append(e)
    entries.sort(key=lambda e: (e['subject'] != '공통', e['subject'], e['number']))
    if limit:
        entries = entries[:limit]
    print(f'  ✓ {len(entries)} 문제 (공통 + 미적분/기하/확률과통계 23-30)', flush=True)

    # 2) 크롭 (ingest_v2/ganah/gyo12 와 동일: 페이지+bbox → crop_problem,
    #    원래 경계 + 위로 headroom 18px. 위첨자 클립 방지·스캔으로 헤더 끌어옴 없음)
    for e in entries:
        name = f'{slug}_{e["subject"]}_{e["number"]:02d}.png'
        img_path = images_dir / name
        e['image_fs'] = f'db/raw/{slug}/images/{name}'
        e['image_url'] = f'/problem-images/{name}'
        e['image_path'] = str(img_path.resolve())    # vision 폴백용 (gyo12/ganah와 동일)
        page_im = Image.open(e['_page_png'])
        if not IV.crop_problem(page_im, e['bbox_px'], img_path, exam_type=EXAM_TYPE):
            page_im.crop(e['bbox_px']).save(img_path)     # degenerate 폴백
        IV._ensure_web_symlink(img_path)
    print(f'  ✓ 크롭 {len(entries)}장', flush=True)

    # 3) 메타데이터 (PDF텍스트 + Haiku, 병렬)
    units = IV.load_concept_index(); meta_cache = raw / 'meta_cache'

    def meta_one(e):
        # 메타 실패(예: claude 인증 401·타임아웃)는 *비치명적* — 빈 meta로 강등하고 계속.
        # 한 문항 실패가 회차 오케스트레이터를 죽이면 안 된다. (gyo12 meta_one 패턴)
        m = {}
        try:
            m = IV.extract_metadata(
                pdf_path=e['_pdf'], page_num=e['page_num'], bbox_pdf=e['bbox_pdf'],
                number=e['number'], subject=e['subject'], units_index=units,
                cache_dir=meta_cache, cache_key=f'{e["subject"]}_{e["number"]:02d}', timeout=60,
                                # ★이미지 직독 + 과목/학년/연도 스코프 — 텍스트레이어는 지수를 뭉갠다
                                image_path=Path(e['image_path']) if e.get('image_path') else None,
                                grade=e.get('grade'), year=e.get('year'))
            # PUA 특수기호(벡터 화살표 등)로 텍스트 메타가 searchable_text를 비우면 → 이미지 vision 폴백
            if not (isinstance(m, dict) and len((m.get('searchable_text') or '').strip()) >= 10):
                import vision_meta
                m2 = vision_meta.extract_metadata(Path(e['image_path']), units,  # Path 필수(.stem)
                                                  cache_dir=meta_cache, timeout=90)
                if m2 and (m2.get('searchable_text') or '').strip():
                    m = m2
        except Exception as ex:
            print(f'  ⚠ meta 강등 {e["subject"]} #{e["number"]:02d}: {type(ex).__name__}: {str(ex)[:80]}', flush=True)
            m = m if isinstance(m, dict) else {}
        return e, m
    nfail = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('META_WORKERS', '20'))) as ex:
        for e, m in ex.map(meta_one, entries):
            e['meta'] = m
            if not (isinstance(m, dict) and m.get('unit')):
                nfail += 1
    print(f'  ✓ 메타데이터 (unit실패 {nfail})', flush=True)

    # 4) 정답 — 해설 정답표 (결정론, 비전0)
    flat = A.parse_haesol_answers({s: raw / f'{s}_해설.pdf' for s in SELECTIVES})
    answers: dict = {}
    for (s, n), a in flat.items():
        answers.setdefault(s, {})[str(n)] = a
    print(f'  ✓ 정답 {sum(len(v) for v in answers.values())}개 (해설 정답표)', flush=True)
    # 🔴 개수 게이트 (gyo12 len==30·ganah got==30 대응): 공통 22 + 각 선택 8.
    #    parse_haesol_answers가 한 과목 정답을 조용히 누락해도 ans=None으로 박히는 것을 시끄럽게.
    got_common = len(answers.get('공통', {}))
    assert got_common == 22, f"🔴 공통 정답 {got_common}개 (22 아님) — 해설 정답표 파싱 점검"
    for s in SELECTIVES:
        got = len(answers.get(s, {}))
        assert got == 8, f"🔴 {s} 선택 정답 {got}개 (8 아님) — 해설 정답표 파싱 점검"
    A.assert_selectives_distinct(answers)   # 🔴 안전장치: 선택 3과목 답 동일하면 중단
    print('  ✓ 안전장치 통과 (선택 3과목 distinct)', flush=True)

    # 5) markdown + DB
    written = []
    for e in entries:
        subj, num = e['subject'], e['number']
        ans = answers.get(subj, {}).get(str(num))
        meta = e.get('meta') or {}
        prob = {'subject': subj, 'number': num,
                'score': IV._guess_score(num, EXAM_TYPE, grade),
                'format': _fmt_by_num(num), 'body': '',   # 시험구조상 고정(Haiku 분류 무시)
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
        print(f'  [{num:>2}] {subj:>10} ans={ans!s:>4} unit={meta.get("unit","?")}', flush=True)

    IV.db_upsert(written, year, EXAM_TYPE, session,
                 f'db/raw/{slug}/미적분_문제.pdf', grade=grade, agency=AGENCY)
    print(f'  ✓ DB upsert {len(written)}문제', flush=True)
    return {'round': slug, 'ok': True, 'count': len(written)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, required=True)
    ap.add_argument('--session', required=True)
    ap.add_argument('--grade', default='고3')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--with-cache', action='store_true', help='인제스트 후 풀이 캐시까지 (ganah/gyo12 와 동일)')
    ap.add_argument('--no-sync', action='store_true',
                    help='후처리 동기화(post_ingest_sync) 생략 — orchestrate가 일괄 처리할 때 사용')
    a = ap.parse_args()
    result = ingest(a.year, a.session, a.grade, a.limit)
    print(json.dumps(result, ensure_ascii=False))
    if result.get('ok'):
        md_dir = ROOT / 'docs' / 'problems' / str(a.year) / result['round'].split('_', 1)[1]
        slugs = sorted(p.stem for p in md_dir.glob('*.md'))
        # 텍스트 품질·정합성 게이트 (캐시/동기화 전 — ganah/gyo12 와 동일):
        # PUA 손상 searchable_text 자동 재전사 + format 오분류 자동교정.
        if slugs:
            print(f'\n══════ 텍스트 품질·정합성 게이트 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'text_quality_gate.py'),
                            '--list', ','.join(slugs)])
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'consistency_gate.py'),
                            '--list', ','.join(slugs), '--fix'])
        if a.with_cache:
            print(f'\n══════ 풀이 캐시 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_solution_cache.py'),
                            '--list', ','.join(slugs), '--parallel', '20'])
    # 파이프라인: markdown 작성 후 개념 역인덱스·그래프 재생성 + dev 콘텐츠 리프레시 (안 하면 stale)
    if not a.no_sync:
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent.parent / 'post_ingest_sync.py')],
                       env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
