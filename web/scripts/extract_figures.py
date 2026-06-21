#!/usr/bin/env python3
"""기출 문제 그림 자동 추출 + placeholder 삽입.

사용: python extract_figures.py <round> <subj> <num> [--apply]
  PDF에서 문제 영역 자동 탐지 → 이미지 객체 클러스터(인접 병합) + 캡션([그림N]) 크롭 →
  web/public/problem-images/ 저장(흰여백 trim) → 이미지 위 텍스트를 앵커로
  기존 searchable_text(숫자 보존)에 {{FIGn}} placeholder 삽입 → md frontmatter 갱신.
  --apply 없으면 dry-run(출력만).
"""
import fitz, json, re, sys, os
from PIL import Image, ImageChops

REPO = '/home/insung/Projects/math-study'
PUB = f'{REPO}/web/public/problem-images'
sys.path.insert(0, f'{REPO}/scripts/ingest_kice')
try:  # 표 셀의 한컴 PUA 폰트 디코드(hancom_rosetta 사전)
    from hancom_decode import decode_str, load_rosetta
    _ROSETTA = load_rosetta()
except Exception:
    decode_str = lambda s, t=None: s; _ROSETTA = {}


def merge(rects, gap=20):
    rects = sorted([+r for r in rects], key=lambda r: (r.y0, r.x0))
    cl = []
    for r in rects:
        hit = None
        for c in cl:
            if not (r.x0 > c.x1 + gap or r.x1 < c.x0 - gap or r.y0 > c.y1 + gap or r.y1 < c.y0 - gap):
                hit = c; break
        if hit: hit.include_rect(r)
        else: cl.append(+r)
    return cl


def spans_of(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l.get('spans', []):
                t = s['text'].strip()
                if t: out.append((t, fitz.Rect(s['bbox'])))
    return out


def find_region(doc, num):
    """번호 'num.' 위치로 문제 영역(단 경계 + 다음 번호까지) 탐지. 문제 마커 = 마침표 'N.' + 컬럼 좌측 edge
    (x0≈88 좌단 / 429 우단). 페이지 헤더 '10월'·본문 중간 stray 숫자(마침표X·비edge)에 오매치해 엉뚱한 페이지
    잡던 버그 수정. 1차 마침표 필수(엄격), 못 찾으면 2차 마침표 옵션 폴백(마커에 마침표 없는 회차 대비). 둘 다 edge."""
    def edge(r, PW): return r.x0 < 110 or PW / 2 - 5 <= r.x0 < PW / 2 + 110
    for require_dot in (True, False):
        for pi, page in enumerate(doc):
            sp = spans_of(page); PW = page.rect.width
            pat = rf'^{num}\.$' if require_dot else rf'^{num}\.?$'
            tgt = next((r for t, r in sp if re.match(pat, t.strip()) and edge(r, PW)), None)
            if not tgt: continue
            x0, x1 = (0, PW / 2) if tgt.x0 < PW / 2 else (PW / 2, PW)  # 좌/우 단
            # 같은 단 아래쪽 다음 마커(마침표+edge) = 영역 끝. 없으면 page 끝.
            cands = [r.y0 for t, r in sp if re.match(r'^\d+\.$', t.strip())
                     and x0 - 5 <= r.x0 < x1 and edge(r, PW) and r.y0 > tgt.y1 + 5]
            y1 = min(cands) if cands else page.rect.y1
            return pi, fitz.Rect(x0, tgt.y0 - 3, x1, y1)
    return None, None


def trim(path):
    im = Image.open(path).convert('RGB')
    bg = Image.new('RGB', im.size, im.getpixel((0, 0)))
    bb = ImageChops.difference(im, bg).getbbox()
    if bb: im.crop(bb).save(path)


BOX_NOISE = re.compile(r'선택과목.{0,8}제시|제시되오니|확인하시오|확인\s*사항|답안지')
def classify_box(rows):
    """벡터 격자의 셀 내용으로 박스 종류 판별(339건 measure 기반). placeholder/렌더 타입을 가른다.
       table=데이터표(숫자격자) · proposition=ㄱㄴㄷ보기 · choicebox=(가)(나)빈칸 ·
       condition=조건(•·단일명제) · choices=①~⑤박스 · noise=시험안내문(제거) · passage=본문오인(제거)."""
    cells = [str(c) for row in rows for c in row]
    ne = [c for c in cells if c.strip()]
    if not ne: return 'noise'
    flat = ' '.join(ne)
    fill = len(ne) / max(1, len(cells))
    maxlen = max(len(c) for c in ne)
    if BOX_NOISE.search(flat): return 'noise'                                  # 시험지 안내문/푸터(선택과목 안내)
    if maxlen <= 15 and fill >= 0.55 and re.search(r'\d', flat): return 'table'  # 짧은셀+채움+숫자 = 진짜 데이터표
    if re.search(r'(^|[^가-힣])ㄱ[.\s]', flat) and re.search(r'ㄴ[.\s]', flat): return 'proposition'  # ㄱㄴㄷ 참거짓
    if re.search(r'\((가|나|다|라|마)\)', flat): return 'choicebox'              # (가)(나) 빈칸 채우기
    if re.search(r'[•∙]', flat): return 'condition'                            # 조건 불릿
    if re.search(r'[①②③④⑤]', flat) and maxlen <= 30: return 'choices'          # 선택지 박스
    if maxlen > 25: return 'passage'                                           # 긴 문장 = 본문 격자 오인
    return 'condition'                                                         # 짧은 단일셀 명제류


def extract_table(page, REG):
    """벡터 격자 → {type, rows, bbox}. type=classify_box(rows). 셀 값은 hancom_decode(PUA). 격자 없으면 None."""
    PH = page.rect.height
    grid = [d['rect'] for d in page.get_drawings()
            if REG.x0 - 5 <= d['rect'].x0 and d['rect'].x1 <= REG.x1 + 5
            and d['rect'].y0 >= REG.y0 - 5 and d['rect'].y1 <= REG.y1 + 5
            and (d['rect'].y1 - d['rect'].y0) < PH * 0.4]  # 단 경계선(긴 세로) 제외
    vx = sorted(set(round(r.x0) for r in grid if abs(r.x1 - r.x0) < 2))  # 세로 격자선
    hy = sorted(set(round(r.y0) for r in grid if abs(r.y1 - r.y0) < 2))  # 가로 격자선
    if len(vx) < 2 or len(hy) < 2: return None  # 셀 격자 아님
    tb = fitz.Rect(min(vx), min(hy), max(vx), max(hy))
    cells = {}
    for t, r in spans_of(page):
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if not (tb.x0 - 2 <= cx <= tb.x1 + 2 and tb.y0 - 2 <= cy <= tb.y1 + 2): continue
        ci = sum(1 for x in vx if x < cx) - 1; rj = sum(1 for y in hy if y < cy) - 1
        if ci >= 0 and rj >= 0: cells[(rj, ci)] = cells.get((rj, ci), '') + t
    nr, nc = len(hy) - 1, len(vx) - 1
    if nr < 2 or nc < 2: return None  # 1행·1열·단일 셀 = (가)(나) 조건 박스 등 → 데이터 표 아님(표 오인 방지)
    rows = [[decode_str(cells.get((j, i), ''), _ROSETTA) for i in range(nc)] for j in range(nr)]
    # 시험지 푸터("확인 사항 / 답안지 기입")는 문제 표가 아니므로 제외(마지막 문항에 격자로 붙어옴)
    rows = [r for r in rows if not any('확인사항' in c.replace(' ', '') or '답안지' in c for c in r)]
    if not rows: return None
    return {'type': classify_box(rows), 'rows': rows, 'bbox': [round(v) for v in tb]}


def extract(round_, subj, num):
    num = int(num)
    pdf = f'{REPO}/db/raw/{round_}/{subj}_문제.pdf'
    if not os.path.exists(pdf): pdf = f'{REPO}/db/raw/{round_}/문제.pdf'
    doc = fitz.open(pdf)
    pi, REG = find_region(doc, num)
    if REG is None: return None, [], [], '영역 못찾음'
    page = doc[pi]
    seen = set(); objs = []
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if not (REG.x0 - 5 <= r.x0 and r.x1 <= REG.x1 + 5 and r.y0 >= REG.y0 - 5 and r.y1 <= REG.y1 + 5): continue  # 단 경계(x1)까지 — 옆 단 이미지 침투 방지
            k = (round(r.x0), round(r.y0), round(r.x1), round(r.y1))
            if k in seen: continue
            seen.add(k); objs.append((img[0], +r))   # (xref, rect)
    allsp = spans_of(page)
    # 인라인 도형: 본문 줄 안에 박힌 작은 이미지 객체(높이 ≈ 1 텍스트라인 + 좌·우로 본문 한글 인접).
    #   캡처(크롭)는 마진·옆글자 bleed 가 생김 → 임베드 객체를 xref 로 직접 추출(네이티브 경계, bleed 0).
    #   블록 도형(질문↔선택지/우측)과 구분해 {{INLn}} 으로 분류 → reconstruct 가 본문 줄 중간에 인라인 렌더.
    def _is_inline_rect(r):
        if (r.y1 - r.y0) > 30: return False                      # 1 텍스트라인(~13pt) 넘게 크면 블록
        L = R = False
        for t, sp in allsp:
            if not re.search(r'[가-힣]', t): continue              # 본문 한글만
            if sp.y1 <= r.y0 + 2 or sp.y0 >= r.y1 - 2: continue    # y-밴드 안 겹침
            if sp.x1 <= r.x0 + 3: L = True
            if sp.x0 >= r.x1 - 3: R = True
        return L and R
    inline_objs = [(x, r) for x, r in objs if _is_inline_rect(r)]
    block_objs = [(x, r) for x, r in objs if not _is_inline_rect(r)]   # xref 유지(객체추출 판단용)
    # 블록 클러스터링 gap=8: HWP strip(한 도형의 조각, 간격 ~0-3px)은 합치되, 별개 도형(R₁·R₂처럼 간격 10-30px)은
    #   분리 → 각자 객체추출(깨끗). gap=20이면 R₁·R₂가 합쳐져 캡쳐로 빠지고 위 질문줄까지 bleed.
    cl = merge([r for x, r in block_objs], gap=8)
    tbl = extract_table(page, REG)  # 벡터 격자 → {type,rows,bbox}
    # 1단계: 진짜 데이터 표(type=table)만 {{TABLE}} 로 유지. 본문·조건·(가)(나)·보기·시험안내문이
    #   테두리 격자로 오인된 것(classify_box 가 noise/passage/choicebox/… 로 판정)은 placeholder 를
    #   만들지 않는다 — 그 내용은 searchable_text 에 이미 텍스트로 있으므로 본문으로 둔다(박스 렌더는 후속).
    tables = [tbl] if (tbl and tbl.get('type') == 'table') else []
    _box_skip = tbl['type'] if (tbl and tbl.get('type') != 'table') else None
    if not cl and not tables and not inline_objs: return None, [], [], '이미지·표 없음'
    cl = sorted(cl, key=lambda r: (r.y0, r.x0))
    # 캡션 [그림N] 단독을 클러스터에 합집합 (라벨 통째 캡처)
    caps = [(t, r) for t, r in spans_of(page) if re.match(r'^\[그림\s*\d+\]$', t) and REG.x0 - 5 <= r.x0 < REG.x1]
    for c in cl:
        for t, cap in caps:
            if cap.y0 >= c.y1 - 8 and cap.y0 < c.y1 + 52 and cap.x0 < c.x1 and cap.x1 > c.x0:
                c.include_rect(cap)
    # 크롭 + 앵커(클러스터 위 텍스트 블록 끝 문구)
    blocks = [b for b in page.get_text('blocks')  # 단 경계(x1)까지 — 옆 단 블록 침투 방지
              if REG.x0 - 5 <= b[0] and b[2] <= REG.x1 + 5 and b[1] >= REG.y0 - 5 and b[3] <= REG.y1 + 5]
    stem = f'{round_}_{subj}_{num:02d}'
    cmat = fitz.Matrix(220 / 72, 220 / 72); m = 8
    def is_body(b):  # 본문 블록(한글 포함, 캡션 [그림N] 제외)
        return re.search(r'[가-힣]', b[4]) and not re.match(r'^\s*\[그림\s*\d+\]\s*$', b[4].strip())
    def anchor_for(c):  # 좌우 나란히(c 왼쪽에 같은높이 본문)면 본문 끝(선택지 앞), 아니면 바로 위 본문
        side = [b for b in blocks if b[2] <= c.x0 + 5 and b[3] > c.y0 + 3 and b[1] < c.y1 - 3 and is_body(b)]
        if side:
            ko = [b for b in blocks if is_body(b)]; ref = max(ko, key=lambda b: b[3]) if ko else None
        else:
            ab = sorted([b for b in blocks if b[3] <= c.y0 + 5 and is_body(b)], key=lambda b: b[3]); ref = ab[-1] if ab else None
        return re.sub(r'\s+', ' ', ref[4]).strip()[-12:] if ref else ''  # 끝 한글(find_anchor가 앞 떼며 매칭)
    figs = []; inls = []
    os.makedirs(PUB, exist_ok=True)

    def labels_near(c):  # 도형 영역 내·인접의 짧은 라벨 스팬(점·좌표·각도 O·A·B·F₁·π/3 등). 한글/긴 텍스트=본문 제외.
        out = []
        for t, r in allsp:
            if len(t) > 6 or re.search(r'[가-힣]', t):
                continue
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if c.x0 - 18 <= cx <= c.x1 + 18 and c.y0 - 42 <= cy <= c.y1 + 18:
                out.append(r)
        return out
    def _fig_labels(c):  # 반환 (캡쳐 시 포함할 라벨 스팬, 캡쳐 필요?). 도형에 딸린 별도 텍스트 라벨 판별.
        #   내부 라벨(다이어그램 위 텍스트)=넓게 잡음(확실). 외부=라틴 대문자 점라벨(A·B·C·D·O·A_1)만 — PUA 수식조각·
        #   lim·R₁(도형명)·n→∞ 같은 질문/본문 텍스트 오인 방지. 캡션(그림N)도 포함. 본문줄(같은 y행+도형열 한글)은 제외.
        internal, ext_pts, caps = [], [], []
        for t, sp in allsp:
            ts = t.strip()
            if not ts: continue
            cx, cy = (sp.x0 + sp.x1) / 2, (sp.y0 + sp.y1) / 2
            inside = c.x0 <= cx <= c.x1 and c.y0 <= cy <= c.y1
            near = c.x0 - 28 <= cx <= c.x1 + 28 and c.y0 - 28 <= cy <= c.y1 + 28
            if re.match(r'^\[?\s*그림\s*\d', ts):                              # 그림N 캡션
                if near: caps.append(sp)
                continue
            # 도형명 side-caption(R₁·R₂ 등, PUA 인코딩 포함): 도형 좌/우 바깥 + 세로범위 mid + 짧음 → 위치기반
            #   감지(텍스트패턴 무관). lim·n→∞(도형 위쪽)은 세로 mid 아니라 제외. 객체추출해도 캡션은 별도라 잃으니 캡쳐로.
            side = ((c.x0 - 60 <= sp.x1 <= c.x0 + 5) or (c.x1 - 5 <= sp.x0 <= c.x1 + 60)) and c.y0 + 5 <= cy <= c.y1 - 5
            if side and len(ts) <= 5 and not re.search(r'[가-힣]', ts) \
               and not any(re.search(r'[가-힣]', kt) and not (ksp.y1 <= sp.y0 or ksp.y0 >= sp.y1)
                           and ksp.x1 >= c.x0 - 20 and ksp.x0 <= c.x1 + 20 for kt, ksp in allsp):
                caps.append(sp); continue
            if re.search(r'[가-힣]', ts): continue
            if inside and len(ts) <= 4:                                       # 내부 짧은 비한글 = 다이어그램 위 라벨(확실)
                internal.append(sp)
            elif near and not inside and re.match(r"^[A-Z][₀-₉0-9'′]{0,2}$", ts):  # 외부 라틴 대문자 점라벨만
                if not any(re.search(r'[가-힣]', kt) and not (ksp.y1 <= sp.y0 or ksp.y0 >= sp.y1)
                           and ksp.x1 >= c.x0 - 20 and ksp.x0 <= c.x1 + 20 for kt, ksp in allsp):
                    ext_pts.append(sp)                                       # 본문/질문 줄 아닌 고립 점라벨만
        needs = bool(internal) or len(ext_pts) >= 2 or bool(caps)            # 내부라벨 / 외부점라벨≥2 / 캡션 → 캡쳐
        return internal + ext_pts + caps, needs
    for i, c in enumerate(cl):
        # ① 단일 객체 + 딸린 별도 라벨 0(내부·외부·캡션 모두 없음 = 전부 baked-in) → 객체추출(bleed 0).
        # ② 별도 라벨 있음(좌표·캡션이 텍스트로 분리) OR 다중 strip(한컴 분할) OR 추출실패 → 캡쳐(라벨 union 크롭).
        members = [x for x, r in block_objs
                   if c.x0 - 1 <= (r.x0 + r.x1) / 2 <= c.x1 + 1 and c.y0 - 1 <= (r.y0 + r.y1) / 2 <= c.y1 + 1]
        labels, needs_cap = _fig_labels(c)
        fn = None
        if len(members) == 1 and not needs_cap:
            try:                                # ① 객체추출: 임베드 객체 그대로(페이지 캡쳐 아님 → 위 질문줄·옆글자 bleed 0)
                info = doc.extract_image(members[0])
                fn = f'{stem}_fig{i}.{info.get("ext", "png")}'
                with open(f'{PUB}/{fn}', 'wb') as fp:
                    fp.write(info['image'])
            except Exception:
                fn = None                       # 추출 실패 → 캡쳐 폴백
        if fn is None:                          # ② 캡쳐: 딸린 라벨/다중 strip/추출실패 → 라스터 ∪ 라벨 크롭
            region = +c
            for sp in labels:
                region.include_rect(sp)
            clip = (fitz.Rect(region.x0 - m, region.y0 - m, region.x1 + m, region.y1 + m) & page.rect)
            fn = f'{stem}_fig{i}.png'
            page.get_pixmap(matrix=cmat, clip=clip).save(f'{PUB}/{fn}'); trim(f'{PUB}/{fn}')
        figs.append({'image': f'/problem-images/{fn}', 'anchor': anchor_for(c)})
    # 인라인 도형: 임베드 객체를 xref 로 직접 추출(크롭 아님 → 패딩·옆글자 bleed 0). {{INLn}} 으로 본문 줄 중간 삽입.
    def _inline_anchor(r):  # r 왼쪽·같은 y밴드 본문 스팬의 끝 글자 = 본문 줄 중간 삽입 위치
        cands = [(sp, t) for t, sp in allsp
                 if re.search(r'[가-힣]', t) and sp.x1 <= r.x0 + 3
                 and not (sp.y1 <= r.y0 + 2 or sp.y0 >= r.y1 - 2)]
        if not cands: return ''
        sp, t = max(cands, key=lambda c: c[0].x1)
        return re.sub(r'\s+', ' ', t).strip()[-12:]
    for x, r in inline_objs:
        try:
            info = doc.extract_image(x)
            fn = f'{stem}_inl{len(inls)}.{info.get("ext", "png")}'
            with open(f'{PUB}/{fn}', 'wb') as fp:
                fp.write(info['image'])
            inls.append({'image': f'/problem-images/{fn}', 'anchor': _inline_anchor(r)})
        except Exception:
            pass   # 객체 추출 실패 → 인라인 도형 생략(본문 텍스트 묘사로 폴백)
    for tbl in tables:
        tbl['anchor'] = anchor_for(fitz.Rect(tbl['bbox']))
    return figs, inls, tables, None


import glob as _glob


def find_md(round_, subj, num):
    num = int(num); yr = round_.split('_')[0]
    for p in (f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num:02d}.md',
              f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num}.md'):
        g = _glob.glob(p)
        if g: return g[0]
    return None


def apply_md(round_, subj, num, figs, inls, tables):
    """기존 searchable_text에 앵커로 {{FIGn}}(블록)·{{INLn}}(인라인)·{{TABLEn}} 삽입 + frontmatter 갱신."""
    md = find_md(round_, subj, num)
    if not md: return 'md 못찾음'
    txt = open(md, encoding='utf-8').read()
    m = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', txt)
    if not m: return 'searchable_text 없음'
    st = ' '.join(l.strip() for l in m.group(1).splitlines())
    st = re.sub(r'\{\{(?:FIG|INL|TABLE)\d+\}\}', '', st)  # 기존 placeholder 제거
    st = re.sub(r'\\begin\{array\}.*?\\end\{array\}', ' ', st)  # 기존 표 텍스트(array)→{{TABLEn}}로 대체되므로 제거
    st = re.sub(r'\s+', ' ', st).strip()
    def find_anchor(a):  # 앞에서 한 글자씩 떼며 매칭(anchor 앞부분 PUA·불일치 대응), 못 찾으면 본문 끝
        a = a.strip()
        while len(a) >= 4:
            idx = st.find(a)
            if idx >= 0: return idx + len(a)
            a = a[1:]
        return len(st)
    ins = [(find_anchor(f['anchor']), f'FIG{i}') for i, f in enumerate(figs)]
    ins += [(find_anchor(t.get('anchor', '')), f'TABLE{i}') for i, t in enumerate(tables)]
    # 인라인: 같은 앵커("내부에 있는 ⌒")가 본문에 여러 번이면 순서대로 distinct occurrence 에 배치
    #   (이전 INL 위치 이후부터 탐색 → 두 ⌒ 도형이 한 곳에 뭉치지 않음). inls 는 페이지 y-순서.
    _cur = 0
    for i, f in enumerate(inls):
        a = f['anchor'].strip(); pos = -1
        while len(a) >= 4:
            idx = st.find(a, _cur)
            if idx >= 0: pos = idx + len(a); break
            a = a[1:]
        if pos < 0: pos = len(st)
        ins.append((pos, f'INL{i}'))
        _cur = pos
    for pos, tag in sorted(ins, key=lambda x: x[0], reverse=True):  # 뒤에서부터(인덱스 안밀림)
        st = st[:pos] + f' {{{{{tag}}}}} ' + st[pos:]
    # 블록(FIG/TABLE)만 자기 줄로 분리. INL 은 본문 줄 중간에 그대로 둠(인라인 렌더).
    st = re.sub(r'\s*\{\{((?:FIG|TABLE)\d+)\}\}\s*', r'\n{{\1}}\n', re.sub(r'\s+', ' ', st).strip())
    st = re.sub(r' *(\{\{INL\d+\}\}) *', r' \1 ', st)   # INL 주변 공백 정규화(줄 유지)
    block = 'searchable_text: |\n' + '\n'.join('  ' + l for l in st.splitlines()) + '\n'
    txt = txt[:m.start() + 1] + block + txt[m.end():]
    txt = re.sub(r'\nfigures:\n(?:  - .*\n)*', '\n', txt)         # 기존 figures 제거
    txt = re.sub(r'\ninline_figures:\n(?:  - .*\n)*', '\n', txt)  # 기존 inline_figures 제거
    txt = re.sub(r'\ntables:\n(?:  - .*\n)*', '\n', txt)          # 기존 tables 제거
    if inls:
        inlblock = '\n'.join(f'  - image: {f["image"]}' for f in inls)
        txt = re.sub(r'(\nproblem_image: .*\n)', r'\1inline_figures:\n' + inlblock + '\n', txt, count=1)
    if figs:
        figblock = '\n'.join(f'  - image: {f["image"]}' for f in figs)
        txt = re.sub(r'(\nproblem_image: .*\n)', r'\1figures:\n' + figblock + '\n', txt, count=1)
    if tables:
        tblock = '\n'.join('  - ' + json.dumps(t['rows'], ensure_ascii=False) for t in tables)
        txt = re.sub(r'(\nproblem_image: .*\n)', r'\1tables:\n' + tblock + '\n', txt, count=1)
    open(md, 'w', encoding='utf-8').write(txt)
    return None


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--apply']
    do_apply = '--apply' in sys.argv
    figs, inls, tables, err = extract(*args[:3])
    if err: print('FAIL:', err); sys.exit(1)
    print(json.dumps({'figs': figs, 'inls': inls, 'tables': [t['rows'] for t in tables]}, ensure_ascii=False, indent=2))
    if do_apply:
        print('APPLY:', apply_md(*args[:3], figs, inls, tables) or 'OK')
