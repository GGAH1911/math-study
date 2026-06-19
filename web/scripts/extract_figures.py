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
    """번호 'num.' 텍스트 위치로 문제 영역(단 경계 + 다음 번호까지) 탐지."""
    for pi, page in enumerate(doc):
        sp = spans_of(page); PW = page.rect.width
        tgt = next((r for t, r in sp if re.match(rf'^{num}\.?$', t)), None)
        if not tgt: continue
        x0, x1 = (0, PW / 2) if tgt.x0 < PW / 2 else (PW / 2, PW)  # 좌/우 단
        # 같은 단의 아래쪽 다음 번호(어떤 번호든, num+1이 옆 단일 수 있음) = 영역 끝. 없으면 page 끝.
        cands = [r.y0 for t, r in sp if re.match(r'^\d+\.?$', t)
                 and x0 - 5 <= r.x0 < x1 and r.y0 > tgt.y1 + 5]
        y1 = min(cands) if cands else page.rect.y1
        return pi, fitz.Rect(x0, tgt.y0 - 3, x1, y1)
    return None, None


def trim(path):
    im = Image.open(path).convert('RGB')
    bg = Image.new('RGB', im.size, im.getpixel((0, 0)))
    bb = ImageChops.difference(im, bg).getbbox()
    if bb: im.crop(bb).save(path)


def extract_table(page, REG):
    """벡터 격자 표 → {rows:[[...]], bbox}. 셀 값은 hancom_decode(PUA). 표 아니면 None."""
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
    return {'rows': rows, 'bbox': [round(v) for v in tb]}


def extract(round_, subj, num):
    num = int(num)
    pdf = f'{REPO}/db/raw/{round_}/{subj}_문제.pdf'
    if not os.path.exists(pdf): pdf = f'{REPO}/db/raw/{round_}/문제.pdf'
    doc = fitz.open(pdf)
    pi, REG = find_region(doc, num)
    if REG is None: return None, '영역 못찾음'
    page = doc[pi]
    seen = set(); rects = []
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if not (REG.x0 - 5 <= r.x0 and r.x1 <= REG.x1 + 5 and r.y0 >= REG.y0 - 5 and r.y1 <= REG.y1 + 5): continue  # 단 경계(x1)까지 — 옆 단 이미지 침투 방지
            k = (round(r.x0), round(r.y0), round(r.x1), round(r.y1))
            if k in seen: continue
            seen.add(k); rects.append(+r)
    cl = merge(rects)
    tbl = extract_table(page, REG)  # 표(벡터 격자) → table JSON (이미지 크롭 대신 데이터)
    tables = [tbl] if tbl else []
    if not cl and not tables: return None, [], '이미지·표 없음'
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
    figs = []
    os.makedirs(PUB, exist_ok=True)
    for i, c in enumerate(cl):
        clip = (fitz.Rect(c.x0 - m, c.y0 - m, c.x1 + m, c.y1 + m) & page.rect)
        fn = f'{stem}_fig{i}.png'
        page.get_pixmap(matrix=cmat, clip=clip).save(f'{PUB}/{fn}'); trim(f'{PUB}/{fn}')
        figs.append({'image': f'/problem-images/{fn}', 'anchor': anchor_for(c)})
    for tbl in tables:
        tbl['anchor'] = anchor_for(fitz.Rect(tbl['bbox']))
    return figs, tables, None


import glob as _glob


def find_md(round_, subj, num):
    num = int(num); yr = round_.split('_')[0]
    for p in (f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num:02d}.md',
              f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num}.md'):
        g = _glob.glob(p)
        if g: return g[0]
    return None


def apply_md(round_, subj, num, figs, tables):
    """기존 searchable_text에 앵커로 {{FIGn}}·{{TABLEn}} 삽입 + figures/tables frontmatter 갱신."""
    md = find_md(round_, subj, num)
    if not md: return 'md 못찾음'
    txt = open(md, encoding='utf-8').read()
    m = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', txt)
    if not m: return 'searchable_text 없음'
    st = ' '.join(l.strip() for l in m.group(1).splitlines())
    st = re.sub(r'\{\{(?:FIG|TABLE)\d+\}\}', '', st)  # 기존 placeholder 제거
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
    for pos, tag in sorted(ins, key=lambda x: x[0], reverse=True):  # 뒤에서부터(인덱스 안밀림)
        st = st[:pos] + f' {{{{{tag}}}}} ' + st[pos:]
    st = re.sub(r'\s*\{\{((?:FIG|TABLE)\d+)\}\}\s*', r'\n{{\1}}\n', re.sub(r'\s+', ' ', st).strip())
    block = 'searchable_text: |\n' + '\n'.join('  ' + l for l in st.splitlines()) + '\n'
    txt = txt[:m.start() + 1] + block + txt[m.end():]
    txt = re.sub(r'\nfigures:\n(?:  - .*\n)*', '\n', txt)  # 기존 figures 제거
    txt = re.sub(r'\ntables:\n(?:  - .*\n)*', '\n', txt)    # 기존 tables 제거
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
    figs, tables, err = extract(*args[:3])
    if err: print('FAIL:', err); sys.exit(1)
    print(json.dumps({'figs': figs, 'tables': [t['rows'] for t in tables]}, ensure_ascii=False, indent=2))
    if do_apply:
        print('APPLY:', apply_md(*args[:3], figs, tables) or 'OK')
