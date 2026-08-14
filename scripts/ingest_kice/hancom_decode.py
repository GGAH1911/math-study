"""Hancom equation-font PUA decoder — "로제타 스톤".

한국 수능/모의고사 기출 PDF(한컴 HWP 출신)는 수식 글리프를 유니코드 사용자정의영역(PUA,
0xE000~)에 인코딩하고, ToUnicode CMap 도 PUA 로 매핑한다. 그래서 pdftotext/PyMuPDF 로
뽑으면 수식이 깨진다(예: f(x)=2x³-8x → 공백/⋄). 한컴오피스가 있어야만 정상 추출되는 구조.

이 모듈은 **비전으로 검증한 마스터 표**(hancom_rosetta.json, 81종)로 PUA→실제기호를 풀고,
글리프 위치(pdfminer)로 지수/첨자(^{}, _{})를 복원한다. 2020·2021 전 회차/과목에서 미식별 0.

기존 text_meta._PUA_DIGIT_MAP(숫자 10종만 풀고 나머지는 ⋄로 폐기) 의 완전한 대체.
"""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path

_DICT_PATH = Path(__file__).resolve().parent.parent / "hancom_rosetta.json"


def load_rosetta() -> dict[int, str]:
    raw = json.load(open(_DICT_PATH, encoding="utf-8"))
    return {int(k, 16): v for k, v in raw.items()}


ROSETTA: dict[int, str] = load_rosetta()


def _is_pua(o: int) -> bool:
    return 0xE000 <= o <= 0xF8FF or 0xF0000 <= o <= 0xFFFFD


def decode_str(s: str, table: dict[int, str] | None = None) -> str:
    """PUA 글자를 마스터 표로 치환(비-PUA는 그대로)."""
    table = table or ROSETTA
    return "".join(table.get(ord(c), c) if _is_pua(ord(c)) else c for c in s)


def unmapped_pua(s: str, table: dict[int, str] | None = None) -> Counter:
    """표에 없는 PUA 잔여(신규 회차 감지용). 비면 100% 커버."""
    table = table or ROSETTA
    return Counter(c for c in s if _is_pua(ord(c)) and ord(c) not in table)


def decode_structured(
    pdf_path,
    page_num: int | None = None,
    bbox=None,
    table: dict[int, str] | None = None,
):
    """pdfminer 위치기반 디코드 — 지수(^{})·아래첨자(_{}) 복원.

    반환: [(y_top_desc, line_text), ...] 위→아래 순. page_num/bbox 로 영역 한정 가능.
    bbox 는 pdfminer 좌표계(좌하단 원점) (x0, y0, x1, y1).
    """
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTChar, LTTextContainer

    table = table or ROSETTA

    def tr(c: str) -> str:
        o = ord(c)
        return table.get(o, c) if _is_pua(o) else c

    out = []
    for pi, page in enumerate(extract_pages(pdf_path)):
        if page_num is not None and pi != page_num:
            continue
        rows: dict[int, list] = {}
        for el in page:
            if not isinstance(el, LTTextContainer):
                continue
            for line in el:
                if not hasattr(line, "__iter__"):
                    continue
                cs = [c for c in line if isinstance(c, LTChar)]
                if bbox:
                    cs = [c for c in cs if bbox[0] <= c.x0 <= bbox[2] and bbox[1] <= c.y0 <= bbox[3]]
                if not cs:
                    continue
                key = round(sum(c.y0 for c in cs) / len(cs) / 3) * 3  # 3pt 단위로 라인 양자화
                rows.setdefault(key, []).extend(cs)
        for y in sorted(rows, reverse=True):
            cs = sorted(rows[y], key=lambda c: c.x0)
            sizes = sorted(c.size for c in cs)
            main = sizes[len(sizes) // 2] or 1.0
            ybot = min(c.y0 for c in cs)
            buf = ""
            mode = 0  # 0 보통 / 1 위첨자 / -1 아래첨자
            prev_x1 = None
            for c in cs:
                ch = tr(c.get_text())
                # 같은 라인 내 글자 사이 큰 공백 → 띄어쓰기 보존
                if prev_x1 is not None and c.x0 - prev_x1 > main * 0.4 and not buf.endswith(" "):
                    if mode != 0:
                        buf += "}"; mode = 0
                    buf += " "
                prev_x1 = c.x1
                small = c.size < main * 0.85
                up = c.y0 > ybot + main * 0.22
                down = (c.y0 + c.size) < ybot + main * 0.62
                m = 1 if (small and up) else (-1 if (small and down) else 0)
                if m != mode:
                    if mode != 0:
                        buf += "}"
                    if m == 1:
                        buf += "^{"
                    elif m == -1:
                        buf += "_{"
                    mode = m
                buf += ch
            if mode != 0:
                buf += "}"
            out.append((y, buf.strip()))
    return out


def decode_raw_text(pdf_path, table: dict[int, str] | None = None) -> str:
    """빠른 char-level 디코드(구조 평탄). pdftotext -raw 결과를 치환."""
    import subprocess
    raw = subprocess.run(
        ["pdftotext", "-raw", str(pdf_path), "-"], capture_output=True, text=True, timeout=60
    ).stdout
    return decode_str(raw, table)


if __name__ == "__main__":
    import sys
    pdf = sys.argv[1]
    txt = decode_raw_text(pdf)
    un = unmapped_pua(txt)
    print(f"[hancom_decode] 미식별 PUA: {sum(un.values())}회 / {len(un)}종", dict(un.most_common(10)))
    print(txt[:1500])


# ── 기하 구조 파서 (LLM-free): 문제 영역에서 분수·지수·첨자 복원 ──
def _han(s):
    return any('가' <= c <= '힣' for c in s)


def _page_chars_bars(page):
    from pdfminer.layout import LTChar, LTLine, LTRect, LTTextLineHorizontal
    chars = []; bars = []
    def walk(el, lid=0):
        if isinstance(el, LTTextLineHorizontal):
            lid = id(el)
        if isinstance(el, LTChar):
            if not (el.get_text() and ord(el.get_text()[0]) == 0x2501):  # ━ 장식/구분선 제외:
                el._lid = lid; chars.append(el)  # 분수 분자로 오훔침→빈분수(\frac{}{AC})·구분선쓰레기 원천 차단
        elif isinstance(el, LTLine) and abs(el.y1 - el.y0) < 1.5 and abs(el.x1 - el.x0) > 3:
            bars.append((min(el.x0, el.x1), max(el.x0, el.x1), (el.y0 + el.y1) / 2))
        elif isinstance(el, LTRect) and el.height < 2.5 and el.width > 3:
            bars.append((el.x0, el.x1, (el.y0 + el.y1) / 2))
        if hasattr(el, '__iter__'):
            for c in el:
                walk(c, lid)
    walk(page)
    return chars, bars


def _render_line(cs, main):
    cs = sorted(cs, key=lambda c: c.x0)
    base = sorted(c.y0 for c in cs)[len(cs) // 2]
    out = ''; mode = 0; px = None
    for c in cs:
        ch = decode_str(c.get_text())
        if px is not None and c.x0 - px > main * 0.5:
            if mode: out += '}'; mode = 0
            if not out.endswith(' '): out += ' '
        px = c.x1; small = c.size < main * 0.82
        m = 1 if (small and c.y0 > base + main * 0.22) else (-1 if (small and c.y0 + c.size < base + main * 0.55) else 0)
        if m != mode:
            if mode: out += '}'
            out += '^{' if m == 1 else ('_{' if m == -1 else ''); mode = m
        out += ch
    if mode: out += '}'
    return out


_BRACE_CODES = {0xE078, 0xE079, 0xE07A, 0xE07B, 0xE07C, 0xE07D, 0xE07E, 0xE07F, 0xE080,
                0xE081, 0xE082, 0xE083, 0xE084, 0xE100, 0xE102, 0xE103, 0xE104}
# E101·E105 = 단독 절댓값 '|' 글리프(본문크기). 예전엔 _BRACE_CODES에 잘못 포함돼 cases 컬럼이
# 흡수→피스와이즈 구조 붕괴 + 절댓값 소실. 제거하면 rem/절댓값쌍 검출로 흘러가 |…| 로 정상 렌더.
_PIPE_CODES = {0xE101, 0xE105}
# cases(피스와이즈)의 곡선괄호 '{' 글리프. cases 컬럼은 이걸 포함해야 함 —
# ⌈⌊⌉⌋(E100~E104) 각괄호만 있는 건 구간 [a,b]/그룹이지 cases 아님(28번 KaTeX 에러 방지).
_CURLY = {0xE04B, 0xE079, 0xE082}


def _split_rows(body, main):
    # 행 baseline = 본문크기 글자들의 y로 군집 → 모든 글자(분수 포함)를 가까운 행에 배정
    mains = [c for c in body if c.size >= main * 0.9] or body
    ys = sorted(((c.y0 + c.y1) / 2 for c in mains), reverse=True)
    centers = []
    for y in ys:
        if not centers or centers[-1] - y > main * 1.2:
            centers.append(y)
    if len(centers) <= 1:
        return [body]
    out = [[] for _ in centers]
    for c in body:
        cy = (c.y0 + c.y1) / 2
        ri = min(range(len(centers)), key=lambda i: abs(centers[i] - cy))
        out[ri].append(c)
    return [r for r in out if r]


def _cases_groups(chars, main):
    """좌측 큰 브레이스(⎧⎨⎩ 세로컬럼 또는 단일 큰 '{' 글리프 E04B) + 오른쪽 본문 → cases 그룹."""
    braces = sorted([c for c in chars if ord(c.get_text()[0]) in _BRACE_CODES], key=lambda c: c.x0)
    cols = []
    for c in braces:
        for col in cols:
            if abs(c.x0 - col[0].x0) < 10:
                col.append(c); break
        else:
            cols.append([c])
    # 연립방정식 '{' = 단일 큰 곡선브레이스(E04B, size>1.8·main)가 한 글자로 여러 행을 감쌈 → 위 컬럼엔
    # 안 잡혀 누출되던 것. 자체로 한 컬럼 추가. (작은 '{'는 집합 {x|…} 표기라 cases 아님 → 크기로 구분.)
    for c in chars:
        o = ord(c.get_text()[0])
        if o in _CURLY and o not in _BRACE_CODES and c.size > main * 1.8:
            cy0 = (c.y0 + c.y1) / 2  # 연립 '{'는 닫는 '}' 없이 여러 행을 감쌈. 오른쪽·같은 y대역에 닫는 '}'가
            if any(decode_str(d.get_text()) == '}' and d.x0 > c.x1  # 있으면 그룹{…}²·집합{x|…} → cases 아님(그대로 렌더).
                   and abs((d.y0 + d.y1) / 2 - cy0) < main * 3 for d in chars):
                continue
            cols.append([c])
    groups = []
    for col in cols:
        big = len(col) == 1 and col[0].size > main * 1.8 and ord(col[0].get_text()[0]) in _CURLY
        if len(col) < 2 and not big: continue  # 단일 글리프는 cases 아님(큰 단일 곡선브레이스는 예외)
        if not any(ord(c.get_text()[0]) in _CURLY for c in col):
            continue  # 곡선괄호 '{' 없는 컬럼(⌈⌊ 각괄호=구간/그룹)은 cases 아님
        ytop = max(c.y1 for c in col); ybot = min(c.y0 for c in col); bxr = max(c.x1 for c in col)
        body = [c for c in chars if c not in col and c.x0 > bxr - 3
                and ybot - 2 <= (c.y0 + c.y1) / 2 <= ytop + 2 and ord(c.get_text()[0]) not in _BRACE_CODES
                and not _han(decode_str(c.get_text()))]  # 한글(연립 뒤 '의 해를…' 연속문)은 body 아님
        if body:
            groups.append((col, body, min(c.x0 for c in col), (ytop + ybot) / 2))
    return groups


def _bracket_groups(chars):
    """곡선괄호 '{' 없는 brace 컬럼(⌈⌊⌉⌋·큰 ()) = 구간/큰 괄호 델리미터 → [ ] ( ) 단일기호.
    (cases 아니라 _cases_groups 가 건너뛴 것; 28번 닫힌구간 [a,b] 등의 ⌈|⌊...⌉|⌋ 정리.)"""
    braces = sorted([c for c in chars if ord(c.get_text()[0]) in _BRACE_CODES], key=lambda c: c.x0)
    cols = []
    for c in braces:
        for col in cols:
            if abs(c.x0 - col[0].x0) < 10:
                col.append(c); break
        else:
            cols.append([c])
    out = []
    for col in cols:
        if len(col) < 2:
            continue
        if any(ord(c.get_text()[0]) in _CURLY for c in col):
            continue  # cases 곡선괄호 컬럼은 _cases_groups 담당
        syms = {decode_str(c.get_text()) for c in col}
        if syms & {'⌈', '⌊', '['}:
            delim = '['
        elif syms & {'⌉', '⌋', ']'}:
            delim = ']'
        elif syms & {'('}:
            delim = '('
        elif syms & {')'}:
            delim = ')'
        else:
            continue
        cy = (max(c.y1 for c in col) + min(c.y0 for c in col)) / 2
        out.append((col, delim, min(c.x0 for c in col), cy))
    return out


def _lim_groups(chars, main):
    """'lim'/'Lim' + 바로 아래 작은 클러스터(극한변수) → underset 첨자 \\lim_{...}."""
    groups = []
    for a in [c for c in chars if decode_str(c.get_text()).lower() == 'l']:
        acy = (a.y0 + a.y1) / 2
        bs = [c for c in chars if decode_str(c.get_text()) == 'i' and 0 < c.x0 - a.x0 < main * 0.8 and abs((c.y0 + c.y1) / 2 - acy) < 3]
        if not bs:
            continue
        b = min(bs, key=lambda c: c.x0)
        ms = [c for c in chars if decode_str(c.get_text()) == 'm' and 0 < c.x0 - b.x0 < main * 0.8 and abs((c.y0 + c.y1) / 2 - acy) < 3]
        if not ms:
            continue
        m = min(ms, key=lambda c: c.x0)
        lim = [a, b, m]
        sub = [c for c in chars if c not in lim and (c.y0 + c.y1) / 2 < acy - 1
               and acy - (c.y0 + c.y1) / 2 < main * 1.6 and a.x0 - main <= (c.x0 + c.x1) / 2 <= m.x1 + main * 0.5
               and c.size < main * 0.92 and not _han(decode_str(c.get_text()))]
        if sub:
            groups.append((lim, sub, a.x0, acy))
    return groups


_BIGOP = {'∫': '\\int', '∬': '\\iint', '∮': '\\oint', '∑': '\\sum', '∏': '\\prod',
          'Σ': '\\sum', 'Π': '\\prod'}  # 한컴은 합·곱 연산자를 그리스 문자 Σ/Π(U+03A3/U+03A0)로
          # 매핑 → 상하한(작은 글자 위·아래) 있으면 \sum/\prod 로 처리. 상하한 없는 진짜 Σ 문자는 그대로.


def _bigop_groups(chars, main):
    """∫/∑/∏ 등 큰 연산자 + 위·아래 작은 상·하한 → \\int_{}^{} 등.
    적분 하한이 기호 아래(baseline−)로 떨어져 별도 줄로 분리되는 것 방지
    (상한은 기존 첨자로직이 main 라인 안이라 붙지만, 하한은 너무 낮아 줄분리됨)."""
    groups = []
    for s in chars:
        cmd = _BIGOP.get(decode_str(s.get_text()))
        if not cmd:
            continue
        scy = (s.y0 + s.y1) / 2
        # 합·곱(Σ/Π)은 상하한이 기호 위·아래 '중앙' → 좁게(오른쪽 summand 첨자 안 훔치게).
        # 적분(∫)은 상하한이 기호 '오른쪽' → 넓게.
        summ = cmd in ('\\sum', '\\prod')
        xlo = s.x0 - main * 0.3
        xhi = s.x1 + (main * 0.35 if summ else main * 0.95)
        # 다자리 상·하한(p+3 등)이 고정 xhi를 넘어 끝자리가 잘리던 것 → x-인접하면 반복 확장.
        def _cand(_xhi):
            return [c for c in chars if c is not s and c.size < main * 0.85
                    and xlo <= (c.x0 + c.x1) / 2 <= _xhi
                    and abs((c.y0 + c.y1) / 2 - scy) < main * 2.0
                    and not _han(decode_str(c.get_text()))]
        cand = _cand(xhi)
        while True:
            nx = max((c.x1 for c in cand), default=s.x1) + main * 0.3
            if nx <= xhi:
                break
            xhi = nx; cand = _cand(xhi)
        upper = sorted([c for c in cand if (c.y0 + c.y1) / 2 > scy + main * 0.15], key=lambda c: c.x0)
        lower = sorted([c for c in cand if (c.y0 + c.y1) / 2 < scy - main * 0.15], key=lambda c: c.x0)
        if upper or lower:
            groups.append((s, cmd, upper, lower, s.x0, scy))
    return groups


_BAR_CODE = 0xE06D  # 한컴 '가로줄' 글리프 — 분수선·근호윗줄·선분윗줄 공용. E046(진짜 마이너스)와
                    # 별개 코드인데 rosetta가 둘 다 '-'로 매핑 → 여기서 코드로 직접 구분(추측 기하 대신).


def _is_bar(c):
    # E06D(기존 바 코드) + '‾' 로 매핑된 신규 바 코드(rosetta_extend가 구조 가로줄을 '‾'로 식별) 둘 다 인식.
    t = c.get_text()
    return bool(t) and (ord(t[0]) == _BAR_CODE or decode_str(t) == '‾')


_MATRIX_LB = 0xE044  # 큰(다중행) 좌괄호 글리프 — 일반 '(' E044와 같은 코드지만 size>1.5*main 로 구분
_MATRIX_RB = 0xE045  # 큰 우괄호


def _matrix_groups(chars, main):
    """큰 괄호(E044/E045, size>1.5*main) + 내부 2행 이상 격자 → 행렬."""
    lefts = [c for c in chars if c.get_text() and ord(c.get_text()[0]) == _MATRIX_LB and c.size > 1.5 * main]
    rights = [c for c in chars if c.get_text() and ord(c.get_text()[0]) == _MATRIX_RB and c.size > 1.5 * main]
    groups = []
    for lb in sorted(lefts, key=lambda c: c.x0):
        rb_cands = [c for c in rights if abs(c.y0 - lb.y0) < 2 and abs(c.y1 - lb.y1) < 2 and c.x0 > lb.x1]
        if not rb_cands:
            continue
        rb = min(rb_cands, key=lambda c: c.x0)
        interior = [c for c in chars if c is not lb and c is not rb
                    and lb.x1 - 1 <= c.x0 and c.x1 <= rb.x0 + 1
                    and lb.y0 - 1 <= c.y0 and c.y1 <= lb.y1 + 1]
        if any(_is_bar(c) for c in interior):
            continue  # 분수바(E06D) 있으면 행렬 아님 — 괄호 속 분수쌍(좌표점 (π/6,5/2)·(b_k-1/2))의
                      # 분자=윗행·분모=아랫행을 2×2 격자로 오검출하던 것 차단. (수능엔 행렬 자체가 없음.)
        rows = _split_rows(interior, main)
        if len(rows) >= 2:
            groups.append((lb, rb, rows, lb.x0, (lb.y0 + lb.y1) / 2))
    return groups


def _table_groups(bars):
    """같은 x-range 가로 괘선(LTLine) 3개+ = 표 → 영역 (x0,x1,ylo,yhi; pdfminer 좌표)."""
    from collections import defaultdict
    byx = defaultdict(list)
    for (bx0, bx1, by) in bars:
        byx[(round(bx0 / 4) * 4, round(bx1 / 4) * 4)].append((bx0, bx1, by))
    out = []
    for grp in byx.values():
        if len(grp) < 3:
            continue
        out.append((min(b[0] for b in grp), max(b[1] for b in grp),
                    min(b[2] for b in grp), max(b[2] for b in grp)))
    return out


def _parse(chars, bars, main=None, depth=0, row_sep=None):
    if not chars: return ''
    sizes = sorted(c.size for c in chars); main = main or sizes[len(sizes) // 2] or 10
    xs0 = min(c.x0 for c in chars); xs1 = max(c.x1 for c in chars); rw = xs1 - xs0
    consumed = set(); ph = []
    cx = lambda c: (c.x0 + c.x1) / 2; cy = lambda c: (c.y0 + c.y1) / 2
    # 표: 같은 x-range 가로 괘선 3개+ = 표 영역 → 셀을 행(y)·열(x갭)로 묶어 \begin{array}.
    # 분수보다 먼저 실행 — 표 괘선이 분수바로 오인돼 garbled 분수 되던 것을 원천 차단(셀을 consumed).
    table_regions = _table_groups(bars)
    def _in_table(px, py):
        return any(tx0 - 3 <= px <= tx1 + 3 and tylo - 4 <= py <= tyhi + 4 for (tx0, tx1, tylo, tyhi) in table_regions)
    for (tx0, tx1, tylo, tyhi) in table_regions:
        region = [c for c in chars if id(c) not in consumed and tx0 - 3 <= cx(c) <= tx1 + 3
                  and tylo - 4 <= cy(c) <= tyhi + 4]
        if len(region) < 4:
            continue
        # 한글 비중으로 표 vs 빈칸추론/조건 박스 구분(둘 다 테두리 괘선 있음). 실측: 데이터표 0~10%,
        # 조건박스 20%+ → 임계 0.15. (열 균일성은 표도 헤더 때문에 50%라 판별 불가 → 한글비율이 정답.)
        if sum(1 for c in region if _han(decode_str(c.get_text()))) > len(region) * 0.15:
            continue
        if sum(1 for m in '가나다라마' if any(decode_str(c.get_text()) == m for c in region)) >= 2:
            continue  # (가)(나)(다)… 조건 마커 다수 = 빈칸추론/조건 박스(수식 위주라 한글비율 낮아도)
        cells = [c for c in region if not _han(decode_str(c.get_text()))]
        if len(cells) < 4:
            continue
        cells.sort(key=lambda c: -cy(c)); trows = []; cur = []; ly = None
        for c in cells:
            if ly is not None and ly - cy(c) > main * 0.7:
                trows.append(cur); cur = []
            cur.append(c); ly = cy(c)
        if cur:
            trows.append(cur)
        if len(trows) < 2:
            continue
        rr = []; counts = []
        for row in trows:
            rs = sorted(row, key=lambda c: c.x0); cols = [[rs[0]]]
            for c in rs[1:]:
                if c.x0 - cols[-1][-1].x1 > main * 0.8:
                    cols.append([])
                cols[-1].append(c)
            counts.append(len(cols))
            rr.append(' & '.join(''.join(decode_str(x.get_text()) for x in col) for col in cols))
        if max(counts) < 2:
            continue  # 단일 열만 = 표 아님(세로 나열 등)
        for c in cells:
            consumed.add(id(c))
        ph.append((tx0, (tylo + tyhi) / 2, '\\begin{array}{' + 'c' * max(counts) + '}' + ' \\\\ '.join(rr) + '\\end{array}'))
    # cases(피스와이즈): 큰 브레이스 + 오른쪽 본문을 행별로 분해 → \begin{cases}
    for (col, body, bx, by) in _cases_groups(chars, main):
        if any(id(c) in consumed for c in col): continue
        for c in col + body: consumed.add(id(c))
        rows = _split_rows(body, main)
        # 인터리브 garble 검출: 두 식이 같은 행에 겹치면 그 행에 관계연산자(= < > ≤ ≥)가 2개+ 생김.
        # 정상 cases는 행마다 식 하나 = 관계연산자 1개. 2개+면 인터리브 → 깨진 cases 렌더 말고 평문(이미지 폴백).
        garbled = any(sum(1 for c in r if decode_str(c.get_text()) in '=<>≤≥') >= 2 for r in rows)
        if len(rows) >= 2 and not garbled:  # 행 분리 + 인터리브 아님 → 정상 cases
            inner = _parse(body, bars, main, depth + 1, row_sep=' \\\\ ')  # 본문 _parse(분수 온전) + 행구분 \\
            ph.append((bx, by, '\\begin{cases}' + inner + '\\end{cases}'))
        else:  # 겹침/인터리브 → 평문(연립 키워드로 render가 이미지 폴백)
            ph.append((bx, by, _parse(body, bars, main, depth + 1)))
    # 큰 각괄호/괄호 델리미터(구간 [a,b] 등) → [ ] ( ) 단일기호 (cases 아닌 brace 컬럼).
    for (col, delim, bx, by) in _bracket_groups(chars):
        if any(id(c) in consumed for c in col):
            continue
        for c in col:
            consumed.add(id(c))
        ph.append((bx, by, delim))
    # 행렬: 큰 괄호(E044/E045)+내부 2행 격자 → \begin{pmatrix} (bracket 후·bigop 전, rem이 가져가기 전 소비).
    for (lb, rb, rows, mx, my) in _matrix_groups(chars, main):
        if id(lb) in consumed or id(rb) in consumed or any(id(c) in consumed for c in sum(rows, [])):
            continue
        rowcols = []
        for row in sorted(rows, key=lambda r: -sum(c.y0 + c.y1 for c in r) / len(r)):
            rs = sorted(row, key=lambda c: c.x0); cols = [[rs[0]]]
            for c in rs[1:]:
                if c.x0 - cols[-1][-1].x1 > main * 0.4:
                    cols.append([])
                cols[-1].append(c)
            rowcols.append(cols)
        if min(len(cols) for cols in rowcols) < 2:
            continue  # 모든 행이 ≥2열이라야 행렬(괄호 속 분수식·세로식은 1열 행이 섞여 제외)
        rendered = [' & '.join(_parse(col, bars, main, depth + 1) for col in cols) for cols in rowcols]
        for c in [lb, rb] + sum(rows, []):
            consumed.add(id(c))
        ph.append((mx, my, '\\begin{pmatrix}' + ' \\\\ '.join(rendered) + '\\end{pmatrix}'))
    # 큰 연산자(∫/∑/∏) 상·하한 — 분수블록보다 먼저: summand/integrand 분수가 상하한을 훔쳐가기 전에
    # 연산자가 자기 상하한(작은 글자, 기호 위·아래)을 claim. (∫ 하한이 별도 줄 되는 것도 방지.)
    for (s, cmd, upper, lower, sx, scy) in _bigop_groups(chars, main):
        if id(s) in consumed or any(id(c) in consumed for c in upper + lower):
            continue
        consumed.add(id(s))
        tex = cmd
        if lower:
            for c in lower: consumed.add(id(c))
            tex += '_{' + _parse(lower, bars, None, depth + 1) + '}'  # main=None: 상·하한 작은글자 기준 재계산(지수속 분수 등)
        if upper:
            for c in upper: consumed.add(id(c))
            tex += '^{' + _parse(upper, bars, None, depth + 1) + '}'  # main=None: 상한 작은글자 기준 재계산
        ph.append((sx, scy, tex))
    # 분수바 후보: LTLine/LTRect(괘선 제외) + "−" 글리프(위·아래 모두 글자면 분수선, 없으면 minus 연산자)
    cand = [(bx0, bx1, by, None) for (bx0, bx1, by) in bars
            if not (bx0 < xs0 - 2 or bx1 > xs1 + 2 or (bx1 - bx0) > 0.6 * rw)
            and not _in_table((bx0 + bx1) / 2, by)]  # 표 괘선은 분수바 후보에서 제외
    for c in chars:
        if _is_bar(c):  # E06D 바만 분수바 후보 (E046 마이너스 제외 → 마이너스發 가짜 분수 차단)
            cand.append((c.x0, c.x1, (c.y0 + c.y1) / 2, c))
    for (bx0, bx1, by, dashc) in sorted(cand, key=lambda b: b[2]):
        if dashc is not None and any(
            decode_str(c.get_text()) == '√'
            for c in chars
            if c.x1 - 2 <= dashc.x0 <= c.x1 + 5 and abs((c.y0 + c.y1) / 2 - by) < 8
        ):
            continue  # √ 바로 뒤 바 = 근호 vinculum → 분수 아님(근호 블록이 처리, 윗줄 글자 오훔침 방지)
        cx = lambda c: (c.x0 + c.x1) / 2; cy = lambda c: (c.y0 + c.y1) / 2
        # 분수 판정(결정론): 바에 '맞닿은(resting)' 글자가 위·아래 둘 다 있어야 분수. E06D는 분수선·
        # 선분 vinculum 공용 코드라 '아래 글자 있음'만으로는 선분(\overline)과 구별 불가 → 위에 '맞닿은'
        # 글자(분자)가 있어야 분수. resting = 글자 끝(분자는 바닥 y0, 분모는 천장 y1)이 바 박스 끝에서
        # 0.5·main 이내(한 줄 떨어진 윗줄/아랫줄은 제외). 바 글리프 박스 끝(btop/bbot)을 기준 — 실제 획이
        # 박스 상부라 by(박스 중심)로는 빽빽한 분모가 오거부됐던 게 분수→overline 오판의 원흉이었다.
        # (LTLine 바는 by가 곧 획이라 btop=bbot=by.)
        btop = dashc.y1 if dashc is not None else by
        bbot = dashc.y0 if dashc is not None else by
        inx = lambda c: bx0 - 3 <= cx(c) <= bx1 + 3
        # 분수 전체를 감싸는 큰 괄호(바 위·아래로 동시에 크게 뻗음 ( [ 등)는 분자/분모 아님 → 제외.
        cross = lambda c: c.y0 < by - main * 0.55 and c.y1 > by + main * 0.55
        # resting(분수 판정) 글자는 '본문 크기'여야 함 — 작은 위첨자 ²/아래첨자는 분자/분모 아님.
        # (없으면 \overline{BC}² 가 ²를 분자로 봐서 \frac{2}{BC} 로 오판하던 회귀.) grab(분자/분모 채우기)
        # 시엔 크기제한 없음(x² 분자의 ² 등 포함).
        # big: resting 글자가 '바 자체 크기'(lmain=dashc.size) 기준 본문크기여야 — 작은 위첨자 ²는 제외하되
        # 지수 속 분수(바·분자·분모 다 작음)는 lmain도 작아 정상 인식(LTLine 바는 lmain=main). center 가드:
        # resting 글자 중심이 바에서 main*1.0 이내여야(윗줄/아랫줄 텍스트가 분자/분모로 오인되던 것 차단).
        lmain = dashc.size if dashc is not None else main
        big = lambda c: c.size >= lmain * 0.75
        rest_above = any(c is not dashc and inx(c) and not cross(c) and big(c) and cy(c) > by and c.y0 <= btop + main * 0.5 and cy(c) - by < main * 1.3 and id(c) not in consumed for c in chars)
        rest_below = any(c is not dashc and inx(c) and not cross(c) and big(c) and cy(c) < by and c.y1 >= bbot - main * 0.5 and by - cy(c) < main * 1.3 and id(c) not in consumed for c in chars)
        frac_ok = rest_above and rest_below
        # 분자/분모 grab: 고정창 대신 '연속 밴드 워크' — 바에서 바깥으로 가며 세로 간격이 1.3*main 을
        # 넘으면(=다른 줄) 중단. 단일분수=resting 한 밴드, 중첩분수=연속된 inner 밴드만. 고정창(3.0*main)이
        # 윗줄 본문("2x-" 등)을 분자로 흡수하던 표garble(\frac{x 11}…) 원흉을 결정론적으로 차단. 또 윗줄
        # junk가 섞여 recursion이 중첩분수를 overline 으로 오판하던 것(\frac{\overline{3} 4}…)도 함께 해소.
        def _bandgrab(updir):
            cand_c = sorted(
                [c for c in chars if frac_ok and c is not dashc and inx(c) and not cross(c)
                 and (cy(c) > by if updir else cy(c) < by)
                 and not _han(decode_str(c.get_text())) and id(c) not in consumed],
                key=lambda c: abs(cy(c) - by))
            grabbed = []
            prev = btop if updir else bbot
            for c in cand_c:
                if grabbed and abs(cy(c) - prev) > main * 1.3:
                    break  # 큰 세로 간격 = 다른 줄 → 중단
                grabbed.append(c)
                prev = cy(c)
            return grabbed
        above = _bandgrab(True)
        below = _bandgrab(False)
        na = ''.join(decode_str(c.get_text()) for c in above); nb = ''.join(decode_str(c.get_text()) for c in below)
        if above and below and not _han(na) and not _han(nb):  # 분수: 위·아래 수식(한글 아님)
            pa = _parse(above, bars, main, depth + 1)
            pb = _parse(below, bars, main, depth + 1)
            if pa and pb:  # 빈 분자/분모면 \frac{}{} 가짜노드 생성 안 함(empty_brace 방지)
                for c in above + below: consumed.add(id(c))
                if dashc is not None: consumed.add(id(dashc))
                ph.append(((bx0 + bx1) / 2, by, '\\frac{' + pa + '}{' + pb + '}'))
    # 근호(√) — 분수 뒤에: 분자 속 √((2-√2)/2 등)는 분수가 분자를 claim 후 재귀(_parse)가 처리. 여기선 top-level √.
    for s in sorted([c for c in chars if decode_str(c.get_text()) == '√'], key=lambda c: c.x0):
        if id(s) in consumed: continue
        stop = s.y1
        cands = sorted([c for c in chars if id(c) not in consumed and _is_bar(c)
                        and c.x0 >= s.x0 - 2 and abs((c.y0 + c.y1) / 2 - stop) < 7], key=lambda c: c.x0)
        vinc = []; xend = s.x1  # √에서 연속된 dash만(틈 나면 윗줄 끝)
        for c in cands:
            if c.x0 <= xend + 6:
                vinc.append(c); xend = max(xend, c.x1)
            else:
                break
        if not vinc: continue
        vx1 = xend; vy = min((c.y0 + c.y1) / 2 for c in vinc); vx0 = min(c.x0 for c in vinc)
        rad = [c for c in chars if id(c) not in consumed and c is not s and s.x1 - 4 <= c.x0
               and c.x1 <= vx1 + 3 and s.y0 - 2 < (c.y0 + c.y1) / 2 < vy - 1]
        if rad:
            # 근호 index(∛ 등): √ 갈고리 안(바 시작 vx0 왼쪽)·초소형(size<0.65main; 위첨자 ²는 0.68이라 제외) → \sqrt[n]{}
            idx = [c for c in chars if id(c) not in consumed and c is not s and not _is_bar(c)
                   and s.x0 - 2 <= c.x0 < vx0 and c.size < main * 0.65
                   and s.y0 - 2 <= (c.y0 + c.y1) / 2 <= s.y1 + 3]
            for c in vinc + rad: consumed.add(id(c))
            consumed.add(id(s))
            radtex = _parse(rad, bars, main, depth + 1)
            if idx:
                idx.sort(key=lambda c: c.x0)
                for c in idx: consumed.add(id(c))
                ph.append((s.x0, (s.y0 + s.y1) / 2, '\\sqrt[' + _parse(idx, bars, None, depth + 1) + ']{' + radtex + '}'))  # main=None: 작은 index가 첨자(_{n})로 안 빠지게
            else:
                ph.append((s.x0, (s.y0 + s.y1) / 2, '\\sqrt{' + radtex + '}'))
    # 벡터 액센트: E06D(바)+E06E(→)가 같은 y·x겹침 → \vec{}. (overline 전 — 화살표 동반 바는 선분 아님.)
    for bar in sorted([c for c in chars if _is_bar(c) and id(c) not in consumed], key=lambda c: c.x0):
        bcy = (bar.y0 + bar.y1) / 2
        arrows = [c for c in chars if id(c) not in consumed and c.get_text() and ord(c.get_text()[0]) == 0xE06E
                  and abs(c.y1 - bar.y1) < 1.5 and c.x0 <= bar.x1 + 2]
        if not arrows:
            continue
        arrow = min(arrows, key=lambda c: c.x0)
        # body = 액센트(바+화살표)와 '같은 y밴드'에 겹쳐 얹힌 글자(들)뿐. cy<bcy(바 아래 전부)로 잡으면
        # 아랫줄(②③·다음 식)까지 흡수해 \vec{a 3(②…}로 박살나던 것 → |cy-bcy|<=main 으로 한 밴드만.
        vbody = [c for c in chars if id(c) not in consumed and c is not bar and c.get_text() and ord(c.get_text()[0]) != 0xE06E
                 and bar.x0 - 2 <= (c.x0 + c.x1) / 2 <= arrow.x1 and abs((c.y0 + c.y1) / 2 - bcy) <= main * 1.0
                 and decode_str(c.get_text()) not in ',)(;:=≠+[]'  # 꼬리 연산자/문장부호는 body 아님(액센트 옆)
                 and not _han(decode_str(c.get_text()))]
        if not vbody:
            continue
        consumed.add(id(bar)); consumed.add(id(arrow))
        for c in vbody: consumed.add(id(c))
        ph.append((bar.x0, bcy, '\\vec{' + _parse(vbody, bars, main, depth + 1) + '}'))
    # 선분 \overline: 분수·근호가 안 가져간 E06D 바 중 '아래에만 글자(위·√ 없음)' → \overline{아래}.
    for bar in sorted([c for c in chars if _is_bar(c) and id(c) not in consumed], key=lambda c: c.x0):
        bcx0, bcx1 = bar.x0, bar.x1; bcy = (bar.y0 + bar.y1) / 2
        below = [c for c in chars if id(c) not in consumed and c is not bar
                 and bcx0 - 3 <= (c.x0 + c.x1) / 2 <= bcx1 + 3
                 and bcy - main * 0.95 <= (c.y0 + c.y1) / 2 < bcy
                 and not _han(decode_str(c.get_text()))]
        if not below:
            continue
        if any(decode_str(c.get_text()) == '√' for c in chars
               if c.x1 - 2 <= bar.x0 <= c.x1 + 4 and abs((c.y0 + c.y1) / 2 - bcy) < 8):
            continue  # √ 바로 뒤 = 근호 vinculum(이미 처리) → 선분 아님
        for c in below:
            consumed.add(id(c))
        consumed.add(id(bar))
        ph.append((bar.x0, bcy, '\\overline{' + _parse(below, bars, main, depth + 1) + '}'))
    # 절댓값 |…|: E101/E105 좌우 쌍이 같은 y밴드로 내용을 감싸면 |내용|. (분수 분자 속 |2x-1|은 재귀 _parse가 처리.)
    pipes = sorted([c for c in chars if c.get_text() and ord(c.get_text()[0]) in _PIPE_CODES
                    and id(c) not in consumed and c.size >= main * 0.75], key=lambda c: c.x0)
    used_pipes = set()
    for i, L in enumerate(pipes):
        if id(L) in used_pipes:
            continue
        cyL = (L.y0 + L.y1) / 2
        for R in pipes[i + 1:]:
            if id(R) in used_pipes or R.x0 <= L.x1:
                continue
            if abs((R.y0 + R.y1) / 2 - cyL) > main * 0.5:
                continue
            inner = [c for c in chars if id(c) not in consumed and c is not L and c is not R
                     and L.x1 - 2 <= (c.x0 + c.x1) / 2 <= R.x0 + 2 and abs((c.y0 + c.y1) / 2 - cyL) < main * 0.7]
            if inner:
                for c in [L, R] + inner: consumed.add(id(c))
                used_pipes.add(id(L)); used_pipes.add(id(R))
                ph.append((L.x0, cyL, '|' + _parse(inner, bars, main, depth + 1) + '|'))
                break
    # lim 아래첨자(underset): 'lim'/'Lim' + 바로 아래 작은 클러스터 → \lim_{...}
    for (lim, sub, lx, lcy) in _lim_groups(chars, main):
        if any(id(c) in consumed for c in lim):  # l,i,m 글자가 소비됐으면 lim 토큰 무효
            continue
        sub = [c for c in sub if id(c) not in consumed]  # 분수 분모에 이미 쓰인 첨자는 빼고(전체 그룹 폐기 방지)
        if not sub:
            continue
        for c in lim + sub:
            consumed.add(id(c))
        ph.append((lx, lcy, '\\lim_{' + _parse(sub, bars, None, depth + 1) + '}'))
    rem = [c for c in chars if id(c) not in consumed and not _is_bar(c)]  # 남은 E06D 바는 '-'로 흘리지 말고 폐기
    # 글자 + placeholder(분수/cases)를 한 시퀀스로 → y로 라인 묶고 x로 정렬해 인라인 삽입
    items = [((c.y0 + c.y1) / 2, c.x0, 'c', c) for c in rem] + [(py, px, 'p', t) for (px, py, t) in ph]
    items.sort(key=lambda it: -it[0])
    lines = []; cur = []; lasty = None
    for it in items:
        if lasty is not None and lasty - it[0] > main * 0.7:
            lines.append(cur); cur = []
        cur.append(it); lasty = it[0]
    if cur: lines.append(cur)
    out = []
    for ln in lines:
        ln.sort(key=lambda it: it[1])  # x 순서
        cs = [it[3] for it in ln if it[2] == 'c']
        mc = [c for c in cs if c.size >= main * 0.85 and not _han(decode_str(c.get_text()))] or cs  # baseline은 본문크기 '한글 아닌' 글자 기준(한글이 1pt 낮아 첨자 오판하던 것 방지)
        base = sorted(c.y0 for c in mc)[len(mc) // 2] if mc else 0
        buf = ''; mode = 0; px = None; run = []

        def _flush():
            # 첨자(mode≠0) 런은 _parse 로 재귀 렌더 → 첨자 안의 중첩 위/아래첨자(예: log_{2^{n}})
            # 복원. 본문(mode 0) 런은 글자 그대로(기존 동작 보존). main=None 으로 클러스터 자체
            # baseline 재계산(482/485 의 상·하한 재귀와 동일 패턴).
            nonlocal buf, run
            if not run:
                return
            if mode == 0:
                buf += ''.join(decode_str(cc.get_text()) for cc in run)
            else:
                buf += ('^{' if mode == 1 else '_{') + _parse(run, bars, None, depth + 1) + '}'
            run = []

        for (y, x, kind, pay) in ln:
            if kind == 'p':
                # ★지수 그룹 안의 구조물은 그룹을 닫지 말고 **안에** 넣는다. 예전엔 placeholder 를
                #   만나면 무조건 mode=0 이라 구조물이 ^{} 안에 못 들어갔다 → 5^{-1/2} 가
                #   `5^{-}\frac{1}{2}` 로 샜다(2026 고3 7월 1번). y 중심만으로 판정 — placeholder 는
                #   크기를 안 들고 다닌다. 실측: 지수 +1.09*main · 본문 +0.15~+0.47 → 0.75 로 가른다.
                #   ⚠️아래첨자는 손대지 않는다: 첨자 +0.09 vs 본문 +0.15 라 y 만으론 못 가른다.
                if mode == 1 and (y - base) > main * 0.75:
                    buf += '^{' + (_parse(run, bars, None, depth + 1) if run else '') + pay + '}'
                    run = []; mode = 0; px = None; continue
                _flush(); mode = 0
                buf += pay; px = None; continue
            c = pay
            if px is not None and c.x0 - px > main * 0.5:
                _flush(); mode = 0
                if not buf.endswith(' '): buf += ' '
            px = c.x1; small = c.size < main * 0.82
            m = 1 if (small and c.y0 > base + main * 0.22) else (-1 if (small and c.y0 + c.size < base + main * 0.55) else 0)
            if m != mode:
                _flush(); mode = m
            run.append(c)
        _flush()
        out.append(buf.strip())
    sep = row_sep if row_sep is not None else (' ' if depth else '\n')
    return sep.join(o for o in out if o)


# 시험지 마지막 문제(30번)에 페이지 꼬리로 붙는 답안지 안내 푸터. 30번 bbox 가 페이지 끝까지
# 잡혀 본문에 빨려든다 → 본문이 아니므로 제거. '※/＊/* 확인 사항 … 기입(표기) … 하시오.'
_FOOTER = re.compile(r'\n?[ \t]*[※*＊][ \t]*확인[ \t]*사항.*$', re.S)


def _strip_footer(t: str) -> str:
    return _FOOTER.sub('', t).rstrip()


def decode_problem(pdf_path, page_num, bbox_pdf):
    """문제 영역(bbox.py: 1-index page, top-left bbox_pdf)의 본문을 기하 구조복원으로 디코드."""
    from pdfminer.high_level import extract_pages
    bx0, by0, bx1, by1 = bbox_pdf
    for pi, page in enumerate(extract_pages(pdf_path)):
        if pi != page_num - 1: continue
        H = page.height; chars, bars = _page_chars_bars(page)
        inb = lambda c, x, y: bx0 - 2 <= x <= bx1 + 2 and by0 - 2 <= (H - y) <= by1 + 2
        rc = [c for c in chars if inb(c, (c.x0 + c.x1) / 2, (c.y0 + c.y1) / 2)]
        rb = [b for b in bars if bx0 - 2 <= (b[0] + b[1]) / 2 <= bx1 + 2 and by0 - 2 <= (H - b[2]) <= by1 + 2]
        return _strip_footer(_parse(rc, rb))
    return ''
