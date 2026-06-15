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
import re, sys, os, json, argparse, subprocess
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


def parse_gyo3_ganah(ans_pdf: Path) -> dict:
    """교육청 고3 가/나형 정답표(트랙별 단일 파일) → {num: (answer_str, None)}.

    평가원 가/나형과 달리 (번호 정답) **pair** — 배점·홀짝형 헤더가 없다. 객관식 1-21은
    동그라미/HyhwpEQ PUA 글리프지만, **단답 22-30 인코딩이 회차마다 다르다**:
      · PUA 글리프 (3월형, U+E034~E03D)  · 평문 ASCII 숫자 (4·7월형, '43' '120' 등)
    또 '정답 및 해 설' 제목이 정답표보다 **앞**에 오는 회차(7월)가 있어 단순 '해설' 컷은
    표를 통째로 날린다. → 마커 컷 대신 **번호 1→30 순증 연속**으로 정답표를 직접 식별한다
    (해설 본문은 번호가 1,2,3… 순증하지 않아 자연 배제). 단답은 글리프면 _decode_single_ans,
    평문이면 그대로. 전 페이지를 훑어 가장 많이 채운 페이지를 채택(30 도달 시 조기 종료).
    배점은 정답표에 없어 None 반환 → ingest 가 _guess_score 로 채운다.

    ⚠️ 추출기 quirk: 회차마다 단어병합/reading-order 가 달라 한 추출기로는 단답 26-30(나형 7월)
    이나 객관식 8·18(가형 7월) 이 깨진다. → fitz → pdfplumber → find_tables(격자) 순으로 시도하고
    '30개 + 객관식 1-21 ∈ {1..5}' 를 만족하는 첫 결과를 채택한다 (격자선은 순서 혼란을 무시)."""
    import pdfplumber
    from answer_textlayer import _is_ans_glyph, _decode_single_ans

    def _scan(toks: list) -> dict:
        out, expect, i = {}, 1, 0
        while i < len(toks) and expect <= 30:
            t = toks[i]
            if t.isascii() and t.isdigit() and int(t) == expect:   # 정답표 번호는 순증(ascii)
                nxt = toks[i + 1] if i + 1 < len(toks) else ''
                ans = None
                if nxt and all(_is_ans_glyph(c) for c in nxt):     # 글리프(동그라미/PUA)
                    ans = _decode_single_ans(nxt)
                elif expect >= 22 and nxt.isascii() and nxt.isdigit():  # 단답 평문 숫자
                    ans = nxt
                elif nxt in ('-', '‐', '–', '—', '*'):             # 전항정답(모두 정답)
                    ans = '전항정답'
                if ans is not None:
                    out[expect] = (ans, None); expect += 1; i += 2; continue
            i += 1
        return out

    def _valid(d: dict) -> bool:                    # 30개 + 객관식 1-21 ∈ {1..5}
        return len(d) == 30 and all((d.get(n) or ('',))[0] in '12345' for n in range(1, 22))

    best: dict = {}

    def _try(d: dict):
        nonlocal best
        if _valid(d):
            return d
        if len(d) > len(best):
            best = d
        return None

    for page in fitz.open(str(ans_pdf)):            # 1) fitz reading-order (대부분 회차 OK)
        if (r := _try(_scan(page.get_text().split()))) is not None:
            return r
    with pdfplumber.open(str(ans_pdf)) as pp:       # 2) pdfplumber reading-order
        for page in pp.pages:
            if (r := _try(_scan((page.extract_text() or '').split()))) is not None:
                return r
    for page in fitz.open(str(ans_pdf)):            # 3) find_tables 격자 (테두리로 순서 무시)
        for tb in page.find_tables(strategy='lines').tables:
            flat = [(c.strip() if c else '') for row in tb.extract() for c in row]
            if (r := _try(_scan(flat))) is not None:
                return r
    return best


def ingest(year: int, exam_type: str = EXAM_TYPE, session: str | None = None, limit=None,
           agency: str = AGENCY, grade: str | None = None) -> dict:
    if exam_type in ('모평', '모의평가'):
        exam_type = '모의평가'                                     # slugify·bbox·score 가 보는 정식 값
    slug = IV.slugify_round(year, exam_type, session, grade)       # 2021_수능 / 2021_6월모평 / 2020_고3_10월모의고사
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
        page_im = Image.open(e['_page_png'])
        if not IV.crop_problem(page_im, e['bbox_px'], img_path, exam_type=exam_type):
            page_im.crop(e['bbox_px']).save(img_path)     # degenerate 폴백
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

    # 4) 정답 — 수능=통합 정답.pdf(홀수형) / 모평=트랙별(form 없음) / 교육청 고3=트랙별(배점·홀짝 없음, PUA 단답)
    combined = raw / '정답.pdf'
    flat = {}
    if agency == '교육청':                                        # 교육청 고3 가/나형 학평
        for track in TRACKS:
            tp = raw / f'{track}_정답.pdf'
            if tp.exists():
                for num, (ans, sc) in parse_gyo3_ganah(tp).items():
                    flat[(track, num)] = (ans, sc)
    elif combined.exists():
        flat = parse_answers(combined)                            # 수능 통합본
    else:
        for track in TRACKS:                                      # 모평 트랙별 분리본
            tp = raw / f'{track}_정답.pdf'
            if tp.exists():
                for num, (ans, sc) in parse_moapyeong(tp).items():
                    flat[(track, num)] = (ans, sc)
    answers: dict = {}; scores: dict = {}
    for (t, n), (a, s) in flat.items():
        answers.setdefault(t, {})[str(n)] = a
        if s is not None:                                         # 교육청은 배점 없음 → _guess_score 가 채움
            scores[(t, n)] = s
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
        # LLM 슬러그 → 기존 정규 개념 정규화 매칭(중복 stub 방지, 2019 490종 사고 재발 차단)
        us = meta.get('unit') if isinstance(meta, dict) else None
        if us:
            us = IV._canonical_concept(us); meta['unit'] = us
            IV._ensure_concept_exists(us, parent_unit=None, concept_type='unit')
        if isinstance(meta, dict) and meta.get('concepts'):
            meta['concepts'] = [IV._canonical_concept(s) for s in meta['concepts']]
            for sp in meta['concepts']:
                IV._ensure_concept_exists(sp, parent_unit=us, concept_type='definition')
        IV.write_markdown_v2(prob, meta, ans, e['image_url'], e['image_fs'],
                             slug, year, exam_type, session, grade=grade, agency=agency)
        written.append({'prob': prob, 'mapping': meta, 'answer': ans})
        print(f'  [{subj} {num:>2}] ans={ans!s:>4} {prob["format"][:3]} {prob["score"]}점 unit={meta.get("unit","?")}', flush=True)

    IV.db_upsert(written, year, exam_type, session,
                 f'db/raw/{slug}/가형_문제.pdf', grade=grade, agency=agency)
    print(f'  ✓ DB upsert {len(written)}문제', flush=True)
    return {'round': slug, 'ok': True, 'count': len(written)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2021)
    ap.add_argument('--exam-type', default='수능', help='수능 / 모평 / 모의고사(교육청 고3 가나형)')
    ap.add_argument('--session', default=None, help='모평/모의고사면 6월/9월/10월 (수능은 생략)')
    ap.add_argument('--agency', default='평가원', help='평가원 / 교육청(고3 가나형 학평)')
    ap.add_argument('--grade', default=None, help='교육청 고3 가나형이면 고3')
    ap.add_argument('--with-cache', action='store_true', help='인제스트 후 풀이 캐시까지')
    ap.add_argument('--no-sync', action='store_true', help='후처리 동기화 생략')
    ap.add_argument('--limit', type=int, default=None)
    a = ap.parse_args()
    result = ingest(a.year, a.exam_type, a.session, a.limit, agency=a.agency, grade=a.grade)
    print(json.dumps(result, ensure_ascii=False))
    if result.get('ok'):
        slug = result['round']
        md_dir = ROOT / 'docs' / 'problems' / str(a.year) / slug.split('_', 1)[1]
        slugs = sorted(p.stem for p in md_dir.glob('*.md'))
        print(f'\n══════ 텍스트 품질 게이트 {len(slugs)}문제 ══════', flush=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'text_quality_gate.py'),
                        '--list', ','.join(slugs)])           # 손상 searchable_text 자동 재전사 (캐시 전)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'consistency_gate.py'),
                        '--list', ','.join(slugs), '--fix'])  # format 오분류 등 자동교정 (캐시 전)
        if a.with_cache:
            print(f'\n══════ 풀이 캐시 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_solution_cache.py'),
                            '--list', ','.join(slugs), '--parallel', '20'])
        if not a.no_sync:
            print('\n══════ 후처리 동기화 (역인덱스·그래프 + dev 리프레시) ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'post_ingest_sync.py')],
                           env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
        print('\n✓ 파이프라인 완료', flush=True)
