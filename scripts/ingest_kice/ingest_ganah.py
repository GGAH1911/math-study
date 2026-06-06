#!/usr/bin/env python3
"""2021학년도 수능 가형/나형 (계열별 단일트랙 30문항) — 인제스트 어댑터.

옛 수능(가/나형, ~2021학년도)은 공통+선택이 아니라 *계열별 30문항 시험지 2종*이다:
  · 가형(이과): 수Ⅰ·수Ⅱ·미적분·확통, 30문항.   · 나형(문과): 수Ⅰ·수Ⅱ·확통, 30문항.
정답은 텍스트 정답표(가/나 × 홀/짝 4페이지) — **홀수형 기준** 파싱(비전·PUA 0).
공통 문항도 각 폼에 그대로 적재(*중복 인제스트*) — 별개 시험지라 회차 무결성 유지.

데이터 모델: 한 회차 `2021_수능` 안에 subject=가형/나형 (2트랙).
스테이징: db/raw/2021_수능/{가형,나형}_문제.pdf + 정답.pdf
사용: python ingest_ganah.py --year 2021 [--with-cache] [--no-sync] [--limit N]
기존 ingest_v2 헬퍼만 재사용(회귀0). MATHSTUDY_ROOT 로 워크트리 오버라이드.
"""
from __future__ import annotations
import sys, os, json, argparse, subprocess
from pathlib import Path
import concurrent.futures as cf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_v2 as IV          # noqa: E402  render/bbox/crop/meta/md/db 헬퍼
from PIL import Image           # noqa: E402
import fitz                     # noqa: E402

ROOT = IV.ROOT
TRACKS = ['가형', '나형']
EXAM_TYPE = '수능'
AGENCY = '평가원'
CIRCLED = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}


def _fmt(n: int) -> str:
    """format은 시험구조상 고정: 1~21 객관식, 22~30 단답형 (문제 안 보고 번호로)."""
    return 'choice' if 1 <= n <= 21 else 'numeric'


def parse_answers(ans_pdf: Path, form: str = '홀수') -> dict:
    """가/나형 정답표 → {(track, num): (answer_str, score)}. 텍스트 (문항,정답,배점) triplet, 홀수형."""
    doc = fitz.open(str(ans_pdf))
    out: dict = {}
    for page in doc:
        txt = page.get_text()
        head = ' '.join(txt[:160].split())
        track = next((t for t in TRACKS if t in head), None)
        if not track or form not in head:          # 짝수형/타과목 페이지 스킵
            continue
        toks = [t for t in txt.split() if t.isdigit() or t in CIRCLED]   # 제목·헤더 제거
        i, n, seen = 0, len(toks), set()
        while i + 2 < n:
            a, b, c = toks[i], toks[i + 1], toks[i + 2]   # (문항번호, 정답, 배점)
            if a.isdigit() and 1 <= int(a) <= 30 and c.isdigit() and int(c) in (2, 3, 4) and int(a) not in seen:
                num = int(a); seen.add(num)
                out[(track, num)] = (CIRCLED.get(b, b), int(c))
                i += 3
            else:
                i += 1                              # 미정렬 → 한 칸 재동기
    return out


def parse_moapyeong(ans_pdf: Path) -> dict:
    """모평 정답표(트랙별 단일 파일, 홀/짝 form 없음) → {num: (answer_str, score)}.
    (문항 정답 배점) triplet 4열 그리드. parse_answers 와 달리 form·track 헤더에 의존하지 않는다
    (모평은 가형/나형 정답이 별도 파일이라 한 파일에 한 트랙뿐). 배점합=100 으로 무결성 검증.
    (2021 6·9월모평 가/나 4파일 × 30 = 120답 실측 30/30·배점합100.)"""
    doc = fitz.open(str(ans_pdf))
    out: dict = {}
    for page in doc:
        toks = [t for t in page.get_text().split() if t.isdigit() or t in CIRCLED]
        i, n, seen = 0, len(toks), set()
        while i + 2 < n:
            a, b, c = toks[i], toks[i + 1], toks[i + 2]   # (문항번호, 정답, 배점)
            if a.isdigit() and 1 <= int(a) <= 30 and c.isdigit() and int(c) in (2, 3, 4) and int(a) not in seen:
                num = int(a); seen.add(num); out[num] = (CIRCLED.get(b, b), int(c)); i += 3
            else:
                i += 1
    return out


def ingest(year: int, exam_type: str = EXAM_TYPE, session: str | None = None, limit=None) -> dict:
    if exam_type in ('모평', '모의평가'):
        exam_type = '모의평가'                                     # slugify·bbox·score 가 보는 정식 값
    slug = IV.slugify_round(year, exam_type, session, None)        # 2021_수능 / 2021_6월모평
    raw = ROOT / 'db' / 'raw' / slug
    images_dir = raw / 'images'; images_dir.mkdir(parents=True, exist_ok=True)
    print(f'══════ {slug} (가/나형 어댑터: {exam_type}{" " + session if session else ""}) ══════', flush=True)

    # 1) 트랙별 PDF: render + bbox(30) + relabel subject=track
    entries = []
    for track in TRACKS:
        pdf = raw / f'{track}_문제.pdf'
        if not pdf.exists():
            print(f'  ⚠ 없음: {pdf.name}', flush=True); continue
        pages = IV.render_pdf_pages(pdf, raw / f'pages_{track}')
        page_by_num = {int(p.stem[1:]): p for p in pages}
        for e in IV.extract_problem_bboxes(pdf, exam_type, session):
            e['subject'] = track                    # bbox는 '공통'으로 찍지만 트랙이 맞다
            e['_pdf'] = pdf
            e['_page_png'] = page_by_num.get(e['page_num'])
            entries.append(e)
    entries.sort(key=lambda e: (e['subject'], e['number']))
    if limit:
        entries = entries[:limit]
    print(f'  ✓ {len(entries)} 문제 (가형/나형 각 30)', flush=True)

    # 2) 크롭
    for e in entries:
        name = f'{slug}_{e["subject"]}_{e["number"]:02d}.png'
        img_path = images_dir / name
        e['image_fs'] = f'db/raw/{slug}/images/{name}'
        e['image_url'] = f'/problem-images/{name}'
        e['image_path'] = str(img_path.resolve())   # vision 폴백용
        cand = Image.open(e['_page_png']).crop(e['bbox_px'])
        tmp = images_dir / f'.cand_{e["subject"]}_{e["number"]:02d}.png'; cand.save(tmp)
        try:
            if not IV.crop_by_gap(tmp, img_path, exam_type=exam_type):
                cand.save(img_path)
        finally:
            tmp.unlink(missing_ok=True)
        IV._ensure_web_symlink(img_path)
    print(f'  ✓ 크롭 {len(entries)}장', flush=True)

    # 3) 메타데이터 (PDF텍스트+Haiku, 병렬, vision 폴백)
    units = IV.load_concept_index(); meta_cache = raw / 'meta_cache'

    def meta_one(e):
        m = IV.extract_metadata(pdf_path=e['_pdf'], page_num=e['page_num'], bbox_pdf=e['bbox_pdf'],
                                number=e['number'], subject=e['subject'], units_index=units,
                                cache_dir=meta_cache, cache_key=f'{e["subject"]}_{e["number"]:02d}', timeout=60)
        if not (isinstance(m, dict) and len((m.get('searchable_text') or '').strip()) >= 10):
            import vision_meta
            m2 = vision_meta.extract_metadata(Path(e['image_path']), units, cache_dir=meta_cache, timeout=90)  # Path 필수(.stem)
            if m2 and (m2.get('searchable_text') or '').strip():
                m = m2
        return e, m
    nfail = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('META_WORKERS', '20'))) as ex:
        for e, m in ex.map(meta_one, entries):
            e['meta'] = m
            if not (isinstance(m, dict) and m.get('unit')):
                nfail += 1
    print(f'  ✓ 메타데이터 (unit실패 {nfail})', flush=True)

    # 4) 정답 — 수능=통합 정답.pdf(홀수형) / 모평=트랙별 {가형,나형}_정답.pdf(form 없음) + 안전장치
    combined = raw / '정답.pdf'
    if combined.exists():
        flat = parse_answers(combined)                            # 수능 통합본
    else:
        flat = {}
        for track in TRACKS:                                      # 모평 트랙별 분리본
            tp = raw / f'{track}_정답.pdf'
            if tp.exists():
                for num, (ans, sc) in parse_moapyeong(tp).items():
                    flat[(track, num)] = (ans, sc)
    answers: dict = {}; scores: dict = {}
    for (t, n), (a, s) in flat.items():
        answers.setdefault(t, {})[str(n)] = a; scores[(t, n)] = s
    for t in TRACKS:
        got = len(answers.get(t, {}))
        assert got == 30, f"🔴 {t} 정답 {got}개 (30 아님) — 정답표 파싱 점검"
    if answers.get('가형') == answers.get('나형'):
        raise AssertionError("🔴 가형==나형 정답 동일 — 파싱 버그 (별개 시험인데 같을 수 없음)")
    print(f'  ✓ 정답 {sum(len(v) for v in answers.values())}개 (가/나형 홀수형, distinct)', flush=True)

    # 5) markdown + DB
    written = []
    for e in entries:
        subj, num = e['subject'], e['number']
        ans = answers.get(subj, {}).get(str(num))
        meta = e.get('meta') or {}
        prob = {'subject': subj, 'number': num,
                'score': scores.get((subj, num), IV._guess_score(num, exam_type, None)),
                'format': _fmt(num), 'body': '',
                'image_paths': [e['image_fs']],
                'searchable_text': meta.get('searchable_text', '')}
        us = meta.get('unit') if isinstance(meta, dict) else None
        if us:
            IV._ensure_concept_exists(us, parent_unit=None, concept_type='unit')
        for sp in (meta.get('concepts') or []) if isinstance(meta, dict) else []:
            IV._ensure_concept_exists(sp, parent_unit=us, concept_type='definition')
        IV.write_markdown_v2(prob, meta, ans, e['image_url'], e['image_fs'],
                             slug, year, exam_type, session, grade=None, agency=AGENCY)
        written.append({'prob': prob, 'mapping': meta, 'answer': ans})
        print(f'  [{subj} {num:>2}] ans={ans!s:>4} {prob["format"][:3]} {prob["score"]}점 unit={meta.get("unit","?")}', flush=True)

    IV.db_upsert(written, year, exam_type, session,
                 f'db/raw/{slug}/가형_문제.pdf', grade=None, agency=AGENCY)
    print(f'  ✓ DB upsert {len(written)}문제', flush=True)
    return {'round': slug, 'ok': True, 'count': len(written)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2021)
    ap.add_argument('--exam-type', default='수능', help='수능 / 모평')
    ap.add_argument('--session', default=None, help='모평이면 6월/9월 (수능은 생략)')
    ap.add_argument('--with-cache', action='store_true', help='인제스트 후 풀이 캐시까지')
    ap.add_argument('--no-sync', action='store_true', help='후처리 동기화 생략')
    ap.add_argument('--limit', type=int, default=None)
    a = ap.parse_args()
    result = ingest(a.year, a.exam_type, a.session, a.limit)
    print(json.dumps(result, ensure_ascii=False))
    if result.get('ok'):
        if a.with_cache:
            slug = result['round']
            md_dir = ROOT / 'docs' / 'problems' / str(a.year) / slug.split('_', 1)[1]
            slugs = sorted(p.stem for p in md_dir.glob('*.md'))
            print(f'\n══════ 풀이 캐시 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_solution_cache.py'),
                            '--list', ','.join(slugs), '--parallel', '20'])
        if not a.no_sync:
            print('\n══════ 후처리 동기화 (역인덱스·그래프 + dev 리프레시) ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'post_ingest_sync.py')],
                           env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
        print('\n✓ 파이프라인 완료', flush=True)
