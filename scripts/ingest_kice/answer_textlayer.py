"""평가원 수능/모평 정답표 텍스트레이어 파싱 (좌표 기반).

비전 LLM 파싱(extract_answers)이 '공통+선택 3과목' 다중컬럼 정답표에서 자주
틀린다 (선택 3과목 칸에 같은 컬럼을 복사, 공통 누락 등 — 2027_6월모평 실측 10/46).
정답표 PDF에 텍스트 레이어가 있으면 좌표 기반으로 정확히(=46/46) 뽑는다.

표 구조: 각 데이터 행 = (문항번호, 정답, 배점) 묶음이 좌→우로 나열.
  · 공통 1~22  (보통 2개 서브컬럼: 1-11, 12-22)
  · 선택 23~30 × 3과목  (헤더 x순서로 과목 매핑)
정답: ①~⑤ → '1'~'5', 단답형은 숫자 문자열 그대로.

반환: {(subject, number): answer_str}.  subject ∈ {'공통','미적분','확률과통계','기하'}.
"""
import re
from collections import defaultdict

import fitz  # PyMuPDF

CIRCLED = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}
# 선택과목 헤더 needle → 정규 subject 명 (기존 데이터 표기와 일치)
_SUBJECT_HEADERS = [('미적분', '미적분'), ('기하', '기하'),
                    ('확률', '확률과통계'), ('통계', '확률과통계')]
_isint = lambda s: bool(re.fullmatch(r'\d+', s))


def has_text_layer(pdf_path, min_chars=80):
    """정답표에 의미있는 텍스트 레이어가 있는지(스캔본 아님)."""
    doc = fitz.open(pdf_path)
    return sum(len(p.get_text().strip()) for p in doc) >= min_chars


def parse_answer_table(pdf_path):
    """평가원 공통+선택 정답표를 {(subject, number): answer} 로 파싱."""
    page = fitz.open(pdf_path)[0]
    words = [(round(w[0], 1), round(w[1], 1), w[4].strip())
             for w in page.get_text("words") if w[4].strip()]

    # y(행) 기준 클러스터링
    rows = defaultdict(list)
    for x, y, t in words:
        key = next((k for k in rows if abs(k - y) <= 6), y)
        rows[key].append((x, t))

    # 데이터행(첫 셀이 1~30 정수) vs 헤더
    data, hdr = [], []
    for y in sorted(rows):
        cells = sorted(rows[y])
        if cells and _isint(cells[0][1]) and 1 <= int(cells[0][1]) <= 30 and len(cells) >= 3:
            data.append(cells)
        else:
            hdr += cells

    # 선택과목을 헤더 x순서대로 (좌→우)
    seen = {}
    for x, t in hdr:
        for needle, subj in _SUBJECT_HEADERS:
            if needle in t and subj not in seen:
                seen[subj] = x
    sel_order = [s for s, _ in sorted(seen.items(), key=lambda kv: kv[1])]

    ans = {}
    for cells in data:
        groups = [cells[i:i + 3] for i in range(0, len(cells) - (len(cells) % 3), 3)]
        si = 0  # 이 행에서 만난 선택 묶음 순번
        for g in groups:
            if len(g) < 3:
                break
            (_xn, n), (_xa, a), (_xs, _sc) = g
            if not _isint(n):
                continue
            n = int(n)
            answer = CIRCLED.get(a, a)
            if n <= 22:
                ans[('공통', n)] = answer
            else:
                # 선택 헤더가 하나라도 미검출(OCR 편차·헤더가 데이터행에 클러스터)되면
                # sel_order 가 짧아져 합성 '선택N' 과목명이 박힌다 → 다운스트림에서 조용히
                # 누락(과목명 불일치)된다. 합성명을 만들지 말고 거부해 ingest_v2 가 vision 으로
                # 폴백하게 한다(try/except 경유). 정확한 textlayer 만 채택.
                if si >= len(sel_order):
                    raise ValueError(
                        f'선택 헤더 미검출: 행에 선택 묶음 {si + 1}개인데 검출 헤더 {len(sel_order)}개 '
                        f'(sel_order={sel_order}) — textlayer 거부, vision 폴백')
                ans[(sel_order[si], n)] = answer
                si += 1
    return ans


# ── 단일과목(교육청 고1/고2 학평·검정고시 등) 해설 PDF 정답 일람표 ────────────
# 객관식 ①~⑤는 텍스트로 나오지만, 단답형 숫자는 HyhwpEQ(한컴 수식폰트) 글리프라
# get_text()엔 '빈칸'으로 보인다. 다만 PDF ToUnicode가 PUA 코드포인트로 매핑해
# 둬서 좌표 텍스트레이어만으로 디코딩 가능하다 (vision·글리프 렌더링 불필요).
#   매핑: U+E034=1, U+E035=2, … U+E03C=9, U+E03D=0  →  digit = (cp-0xE033)%10
# (2026 6월 고1·고2 학평 60문항 실측 100% 검증.)
_PUA_LO, _PUA_HI = 0xe034, 0xe03d
# 일부 회차(2021 11월 학평 등)는 HyhwpEQ 대신 다른 한글 폰트 서브셋을 써서 객관식 ①~⑤가
# 유니코드 동그라미가 아니라 CJK 영역 글리프 U+6ABE~U+6AC2(檾檿櫀櫁櫂)로 들어온다.
# 순차 매핑 ①=U+6ABE … ⑤=U+6AC2 (정답표 렌더 대조로 확정). 이 폰트의 단답은 평문 ASCII.
_CJK_LO, _CJK_HI = 0x6abe, 0x6ac2


def _circled(ch):
    """객관식 동그라미 글리프 → '1'..'5' (해당 없으면 None). 폰트별 코드포인트(유니코드 ①~⑤,
    CJK 서브셋 U+6ABE~)를 한 곳에서 흡수."""
    if ch in CIRCLED:
        return CIRCLED[ch]
    if _CJK_LO <= ord(ch) <= _CJK_HI:
        return str(ord(ch) - _CJK_LO + 1)
    return None


def _is_ans_glyph(ch):
    return _circled(ch) is not None or _PUA_LO <= ord(ch) <= _PUA_HI


def _decode_single_ans(s):
    out = []
    for ch in s:
        c = _circled(ch)
        out.append(c if c is not None else str((ord(ch) - 0xe033) % 10))
    return ''.join(out)


def parse_single_answer_table(pdf_path):
    """단일과목 해설 PDF의 정답 일람표 → {'단일': {번호: 답}}.

    표 = (번호 라벨=ASCII, 정답=①~⑤ 또는 PUA 단답글리프) 밀집 그리드.
    셀 ≥3 인 행(=정답표 행)만 채택하고, 같은 번호는 가장 위(작은 y)를 택해
    본문(해설)의 우발적 (번호→글리프) 오매칭을 배제한다. 좌표/PUA만 사용.
    """
    doc = fitz.open(pdf_path)
    best = {}  # num -> (y, answer)
    try:
        for pno in range(doc.page_count):
            # rawdict 'c' = ToUnicode 문자(PUA 단답글리프 포함). texttrace는
            # 멀티문서 호출에서 C확장 refcount 버그가 있어 rawdict가 안정적.
            d = doc[pno].get_text("rawdict")
            chars = []  # (y, x, ch)
            for blk in d.get('blocks', []):
                for ln in blk.get('lines', []):
                    for sp in ln.get('spans', []):
                        for ch in sp.get('chars', []):
                            c = ch.get('c') or ''
                            if c and ord(c) > 32:
                                ox, oy = ch['origin']
                                chars.append((oy, ox, c))
            chars.sort()
            rows = []
            for y, x, ch in chars:
                if not rows or abs(rows[-1][0] - y) > 3:
                    rows.append([y, []])
                rows[-1][1].append((x, ch))
            for y, cs in rows:
                seq = [ch for _x, ch in sorted(cs)]
                cells, j = [], 0
                while j < len(seq):
                    num = ''
                    while j < len(seq) and seq[j].isascii() and seq[j].isdigit():
                        num += seq[j]; j += 1
                    if not num:
                        j += 1; continue
                    a = ''
                    while j < len(seq) and _is_ans_glyph(seq[j]):
                        a += seq[j]; j += 1
                    if a and 1 <= int(num) <= 30:
                        cells.append((int(num), _decode_single_ans(a)))
                if len(cells) >= 3:  # 정답표 행(밀집 그리드)만
                    for n, ans in cells:
                        if n not in best or y < best[n][0]:
                            best[n] = (y, ans)
    finally:
        doc.close()
    out = {str(n): a for n, (_y, a) in best.items()}
    return {'단일': out} if out else {}


# ── 교육청 고3 (공통+선택) 해설 PDF 정답표 — 내용기반 표탐지 + PUA/평문 ─────────
# 월(교육청)마다 포맷이 다르다: 공통헤더('수학 정답'|'정답'|'2교시 수학 영역'),
# 단답 인코딩(PUA HyhwpEQ ↔ 평문 ASCII), 선택과목 파일구성(통합 부클릿 ↔ 과목별).
# → 과목라벨로 표를 '찾지' 않고, (번호+정답마커) 셀이 있는 행을 *내용*으로 찾는다.
#   공통(1-22)은 PUA좌표+평문시퀀스 둘 다 시도해 병합, 각 선택(23-30)은 자기 파일에서.
# (2021 고3 3·4·7·10월 4회차 × 46문항 = 184답 실측 100% 검증.)

def _ht_chars(page):
    o = []
    for blk in page.get_text("rawdict")['blocks']:
        for ln in blk.get('lines', []):
            for sp in ln.get('spans', []):
                for c in sp.get('chars', []):
                    ch = c.get('c') or ''
                    if ch and ord(ch) > 32:
                        ox, oy = c['origin']
                        o.append((round(oy, 1), round(ox, 1), ch))
    return o


def _ht_rows(chs):
    chs = sorted(chs); rs = []
    for y, x, ch in chs:
        if not rs or abs(rs[-1][0] - y) > 3.5:
            rs.append([y, []])
        rs[-1][1].append((x, ch))
    return [(y, sorted(cs)) for y, cs in rs]


def _ht_cells(items, lo, hi):
    """행에서 (번호, 정답) 셀. 정답마커=①~⑤ 또는 PUA단답글리프. 정답글리프는
    번호 바로 뒤 *연속*(x간격<12)만 취해 다른 칸/풀이 오염을 차단."""
    out = []; i = 0; n = len(items)
    while i < n:
        x, ch = items[i]
        if ch.isascii() and ch.isdigit():
            num = ch; nx = x; i += 1
            while i < n and items[i][1].isascii() and items[i][1].isdigit() and items[i][0] - nx < 12:
                num += items[i][1]; nx = items[i][0]; i += 1
            a = ''
            if i < n and items[i][0] - nx < 24:
                g = items[i][1]
                cg = _circled(g)
                if cg is not None:
                    a = cg; i += 1
                elif _PUA_LO <= ord(g) <= _PUA_HI:
                    a = str((ord(g) - 0xe033) % 10); nx = items[i][0]; i += 1
                    while i < n and _PUA_LO <= ord(items[i][1]) <= _PUA_HI and items[i][0] - nx < 12:
                        a += str((ord(items[i][1]) - 0xe033) % 10); nx = items[i][0]; i += 1
            if a and lo <= int(num) <= hi:
                out.append((int(num), a, x))
        else:
            i += 1
    return out


def _ht_regions(doc):
    """내용서치: (번호+정답마커) 셀을 페이지·컬럼·y연속으로 묶어 '표 영역'들로 분할.
    반환 ([(pno, col, [(y,num,a,x),...]), ...], page_width). col 0=좌단 1=우단."""
    pw = doc[0].rect.width
    groups = {}
    for pno in range(doc.page_count):
        for y, items in _ht_rows(_ht_chars(doc[pno])):
            for num, a, x in _ht_cells(items, 1, 30):
                groups.setdefault((pno, 0 if x < pw / 2 else 1), []).append((y, num, a, x))
    regs = []
    for (pno, col), cs in groups.items():
        cs.sort(); cur = []
        for r in cs:
            if cur and r[0] - cur[-1][0] > 25:   # y간격 크면 다른 표
                regs.append((pno, col, cur)); cur = []
            cur.append(r)
        if cur:
            regs.append((pno, col, cur))
    return regs, pw


def _classify_title(t):
    """표 위 제목 텍스트 → 선택과목명. (공통은 번호범위로 판정하므로 여기선 선택만.)"""
    return ('미적분' if '미적분' in t else '기하' if '기하' in t
            else '확률과통계' if ('확률' in t or '통계' in t) else None)


def _ht_plain(doc, lo, hi):
    """평문 경로: 번호 lo..hi 가 답과 번갈아 나오는 선형 시퀀스(헤더 무관)."""
    for pno in range(doc.page_count):
        t = doc[pno].get_text()
        for ch, dig in CIRCLED.items():
            t = t.replace(ch, f' {dig} ')
        toks = t.split()
        for i in range(len(toks) - 1):
            if toks[i] == str(lo) and toks[i + 1].isdigit():
                got = {}; j = i; e = lo
                while j < len(toks) and e <= hi:
                    if toks[j] == str(e) and j + 1 < len(toks) and toks[j + 1].isdigit():
                        got[e] = toks[j + 1]; e += 1; j += 2
                    else:
                        j += 1
                if len(got) >= min(6, hi - lo + 1):
                    return got
    return {}


def _ht_dec(ch):
    c = _circled(ch)
    if c is not None:
        return c
    if _PUA_LO <= ord(ch) <= _PUA_HI:
        return str((ord(ch) - 0xe033) % 10)
    return ch if (ch.isascii() and ch.isdigit()) else ''


def _ht_plain_seq(text, lo, hi):
    """텍스트에서 번호 lo..hi 순서로 (번호,답) 페어링. get_text가 토큰을 분리해 흡수 없음."""
    for ch, dig in CIRCLED.items():
        text = text.replace(ch, f' {dig} ')
    toks = text.split()
    for i in range(len(toks)):
        if toks[i] == str(lo):
            got = {}; j = i; e = lo
            while j < len(toks) and e <= hi:
                if toks[j] == str(e) and j + 1 < len(toks) and toks[j + 1].isdigit():
                    got[e] = toks[j + 1]; e += 1; j += 2
                else:
                    j += 1
            if len(got) >= min(4, hi - lo + 1):
                return got
    return {}


def _ht_coord_dandab(chs, col, pw, cell_ys, lo, hi):
    """좌표 폴백: 표 행(cell_y) 전체폭, 번호=[lo,hi]범위, 답=다음 번호 시작 x까지.
    전체폭이라 컬럼경계 가로지르는 표(26·27 우측, 답 spillover)도 잡음. 선택은 페이지당 1표라 안전."""
    x0, x1 = (0, pw / 2 + 55) if col == 0 else (pw / 2 - 55, pw)   # 컬럼 + spillover만
    out = {}
    for ty in cell_ys:
        row = sorted((x, ch) for y, x, ch in chs if abs(y - ty) <= 3.5 and x0 <= x < x1)
        nums = []; i = 0; nn = len(row)
        while i < nn:
            x, ch = row[i]
            if ch.isascii() and ch.isdigit():
                v = ch; xe = x; i += 1
                while i < nn and row[i][1].isascii() and row[i][1].isdigit() and row[i][0] - xe < 6 and len(v) < 2:
                    v += row[i][1]; xe = row[i][0]; i += 1
                if lo <= int(v) <= hi:
                    nums.append((xe, int(v)))
            else:
                i += 1
        for k, (xe, num) in enumerate(nums):
            nxt = nums[k + 1][0] - 4 if k + 1 < len(nums) else xe + 45
            a = ''.join(_ht_dec(ch) for x, ch in row if xe < x < nxt)
            if a:
                out.setdefault(num, a)
    return out


def _ht_parse_doc(doc, file_subject, out):
    """해설 PDF 하나 → out{(subj,num):ans} 누적.
    내용서치 → 표 영역 → 표 위 제목 → 파싱. 공통=번호범위(≤22), 선택=제목(없으면 파일과목).
    선택 평문 단답은 표 행만 좁게 get_text(인터리브 풀이 제외) + 좌표 폴백(우측컬럼·인터리브)."""
    regs, pw = _ht_regions(doc)
    chc = {}
    for pno, col, cs in regs:
        nums = set(n for _y, n, _a, _x in cs)
        cell_ys = sorted(set(y for y, _n, _a, _x in cs))
        if max(nums) <= 22:
            subj = '공통'
        elif min(nums) >= 23:                       # 선택 → 표 '바로 위' 제목 읽기
            x0, x1 = (0, pw / 2) if col == 0 else (pw / 2, pw)
            title = doc[pno].get_text("text", clip=fitz.Rect(x0, max(0, min(cell_ys) - 55), x1, min(cell_ys) - 1))
            subj = _classify_title(title) or file_subject
        else:
            continue
        for y, num, a, x in sorted(cs):             # circled/PUA 셀 (최상단)
            out.setdefault((subj, num), a)
        if subj != '공통':                           # 선택 평문 단답
            x0, x1 = (0, pw / 2) if col == 0 else (pw / 2, pw)
            text = ' '.join(doc[pno].get_text("text", clip=fitz.Rect(x0, ty - 3, x1, ty + 4)) for ty in cell_ys)
            for n, v in _ht_plain_seq(text, 23, 30).items():
                out.setdefault((subj, n), v)
            if pno not in chc:
                chc[pno] = _ht_chars(doc[pno])
            for n, v in _ht_coord_dandab(chc[pno], col, pw, cell_ys, 23, 30).items():
                out.setdefault((subj, n), v)
    for n, v in _ht_plain(doc, 1, 22).items():       # 공통 단답 (단일표, 전역)
        out.setdefault(('공통', n), v)


def parse_haesol_answers(haesol_pdfs):
    """교육청 고3 해설 PDF들 → {(subject, number): answer_str}.

    haesol_pdfs: {subject: pdf_path} (예: {'미적분':..., '기하':..., '확률과통계':...}).
    각 파일을 '내용서치 → 표 → 표 위 제목' 순으로 파싱·누적. 통합 부클릿(한 파일에
    공통+3선택)도 과목별 분리본(공통+1선택)도 동일 처리. PUA 좌표 + 평문 병합. 비전 불필요.
    (2021 고3 3·4·7·10월 × 46 = 184답 실측 100%.)
    """
    out = {}
    for subj, pdf in haesol_pdfs.items():
        _ht_parse_doc(fitz.open(pdf), subj, out)
    return out


def _table_single(doc):
    """단일과목 정답표 → {num: ans_str}. PyMuPDF find_tables(테두리 격자)로 셀을 추출한다.

    회차마다 텍스트레이어 레이아웃이 제각각(번호·정답 한 행 인터리브 / 번호행·정답행 분리 /
    2열 packed)이지만 **격자선**이 그걸 무시하고 셀 단위로 끊어주므로 좌표 휴리스틱이 불필요하다.
    셀 = 번호(ascii) | 정답(글리프 ①~⑤·PUA·CJK 또는 평문 ASCII 단답). 번호셀(1..30) 바로 뒤
    셀을 정답으로 페어링 — 글리프면 디코드(_decode_single_ans), 평문이면 그대로. 같은 번호는
    최상단 표 우선(setdefault). (객관식 ①~⑤·CJK 글리프, 단답 PUA·ascii 모두 흡수.)"""
    out = {}
    for pno in range(doc.page_count):
        try:
            tbls = doc[pno].find_tables(strategy="lines").tables
        except Exception:
            continue
        for tb in tbls:
            for row in tb.extract():
                cells = [(c or '').strip() for c in row]
                j = 0
                while j < len(cells) - 1:                  # 번호셀 + 다음 셀(정답) 페어링
                    nc = cells[j]
                    if nc.isdigit() and 1 <= int(nc) <= 30:
                        ac = cells[j + 1]
                        ans = (_decode_single_ans(ac) if ac and all(_is_ans_glyph(ch) for ch in ac)
                               else ac)
                        if ans:
                            out.setdefault(int(nc), ans)
                        j += 2
                    else:
                        j += 1
    return out


def parse_haesol_single(haesol_pdf):
    """단일과목(고1/고2 학평·통합형) 해설 PDF → {('단일', number): answer_str}.

    고3(공통1-22 / 선택23-30)과 달리 단일 30문항(객관식 1-21, 단답 **22**-30). 회차마다
    폰트·레이아웃이 제각각(HyhwpEQ PUA ↔ CJK 글리프 U+6ABE~, 인터리브 ↔ 번호행/정답행 분리,
    PUA 단답 ↔ 평문 ascii)이라 정답표 **격자 테두리**로 셀을 끊는 `_table_single` 로 일괄
    디코드한다. 테두리 없는 표(미검출)는 구 좌표/PUA 경로로 빈 번호만 보강.
    (고1·고2 3·6·9·11월 + 2026 6월 = 30/30 실측.)"""
    doc = fitz.open(str(haesol_pdf))
    g = _table_single(doc)
    if sum(1 for n in g if 1 <= n <= 30) < 30:             # 격자 미검출 → 좌표 폴백으로 빈칸만 채움
        regs, pw = _ht_regions(doc)
        chc = {}
        for pno, col, cs in regs:
            for _y, num, a, _x in sorted(cs):
                g.setdefault(num, a)
            cell_ys = sorted(set(y for y, _n, _a, _x in cs))
            if not cell_ys:
                continue
            if pno not in chc:
                chc[pno] = _ht_chars(doc[pno])
            for n, v in _ht_coord_dandab(chc[pno], col, pw, cell_ys, 22, 30).items():
                g.setdefault(n, v)
    return {('단일', n): a for n, a in g.items()}


def assert_selectives_distinct(answers):
    """안전장치: 선택 3과목(미적분/기하/확률과통계) 정답이 서로 동일하면 AssertionError.
    통합 부클릿 파싱이 한 과목 답을 다른 과목에 복사하는 버그(2021 고3 4·7·10월 실제 발생)를
    인제스트 *전에* 차단한다. answers: {subject: {number_str: answer_str}}.
    - 전체(23-30) 완전 동일 → 버그
    - 단답(객관식 1-5 아닌 답)이 2개 이상 동일 → 버그 (우연 1개 일치는 허용)
    """
    SUBJ = ['미적분', '기하', '확률과통계']
    present = [s for s in SUBJ if answers.get(s)]
    dandab = {s: {n: v for n, v in answers[s].items() if v not in ('1', '2', '3', '4', '5')}
              for s in present}
    full = {s: tuple(answers[s].get(str(n)) for n in range(23, 31)) for s in present}
    for i in range(len(present)):
        for j in range(i + 1, len(present)):
            a, b = present[i], present[j]
            if full[a] == full[b] and any(full[a]):
                raise AssertionError(
                    f"🔴 선택 정답 전체 동일: {a} == {b} = {full[a]} — 파싱 버그. 중단·수정 필요.")
            same = [n for n in (set(dandab[a]) & set(dandab[b])) if dandab[a][n] == dandab[b][n]]
            if len(same) >= 2:
                raise AssertionError(
                    f"🔴 선택 단답 동일: {a} & {b} 단답 {sorted(same)} 모두 일치 "
                    f"({[(n, dandab[a][n]) for n in sorted(same)]}) — 파싱 버그. 중단·수정 필요.")


def is_choice(answer_str):
    """정답이 객관식(①~⑤ 환산 '1'~'5')인지 단답형(그 외 숫자)인지."""
    return answer_str in ('1', '2', '3', '4', '5')


if __name__ == '__main__':
    import sys
    for k, v in sorted(parse_answer_table(sys.argv[1])):
        print(k, v)
