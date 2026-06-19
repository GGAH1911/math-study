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
    # 표(벡터 격자) 감지: 이미지 객체 없는 표 — 짧은 격자선(단 경계선·긴 세로 제외) 묶음을 영역 크롭
    PH = page.rect.height
    grid = [d['rect'] for d in page.get_drawings()
            if REG.x0 - 5 <= d['rect'].x0 and d['rect'].x1 <= REG.x1 + 5
            and d['rect'].y0 >= REG.y0 - 5 and d['rect'].y1 <= REG.y1 + 5
            and (d['rect'].y1 - d['rect'].y0) < PH * 0.4]  # 단 경계선(긴 세로) 제외
    if len(grid) >= 4:  # 격자선 충분 = 표 → 영역을 클러스터로
        gr = fitz.Rect(min(r.x0 for r in grid), min(r.y0 for r in grid), max(r.x1 for r in grid), max(r.y1 for r in grid))
        if gr.width > 30 and gr.height > 20: cl.append(gr)
    if not cl: return None, '이미지 없음'
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
    figs = []
    os.makedirs(PUB, exist_ok=True)
    for i, c in enumerate(cl):
        clip = (fitz.Rect(c.x0 - m, c.y0 - m, c.x1 + m, c.y1 + m) & page.rect)
        fn = f'{stem}_fig{i}.png'
        page.get_pixmap(matrix=cmat, clip=clip).save(f'{PUB}/{fn}'); trim(f'{PUB}/{fn}')
        above = sorted([b for b in blocks if b[3] <= c.y0 + 5  # 그림 위 '한글 포함' 본문 블록(도형 라벨 A·θ 제외)
                        and re.search(r'[가-힣]', b[4])
                        and not re.match(r'^\s*\[그림\s*\d+\]\s*$', b[4].strip())], key=lambda b: b[3])
        # anchor=그림 바로 위 텍스트 끝의 한글(PUA·수식 제외) — searchable_text(디코드본)와 매칭되게
        atxt = re.sub(r'\s+', ' ', re.sub(r'[-]', '', above[-1][4]) if above else '').strip()
        anchor = atxt[-12:] if atxt else ''
        figs.append({'image': f'/problem-images/{fn}', 'anchor': anchor})
    return figs, None


import glob as _glob


def find_md(round_, subj, num):
    num = int(num); yr = round_.split('_')[0]
    for p in (f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num:02d}.md',
              f'{REPO}/docs/problems/{yr}/*/{round_}_{subj}_{num}.md'):
        g = _glob.glob(p)
        if g: return g[0]
    return None


def apply_md(round_, subj, num, figs):
    """기존 searchable_text(숫자 보존)에 앵커로 {{FIGn}} 삽입 + figures frontmatter 갱신."""
    md = find_md(round_, subj, num)
    if not md: return 'md 못찾음'
    txt = open(md, encoding='utf-8').read()
    m = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', txt)
    if not m: return 'searchable_text 없음'
    st = ' '.join(l.strip() for l in m.group(1).splitlines())
    st = re.sub(r'\s+', ' ', re.sub(r'\{\{FIG\d+\}\}', '', st)).strip()  # 기존 placeholder 제거→한 줄
    ins = []
    for i, f in enumerate(figs):
        a = f['anchor'].strip()
        idx = st.find(a) if a else -1
        ins.append((idx + len(a) if idx >= 0 else len(st), i))
    for pos, i in sorted(ins, reverse=True):  # 뒤에서부터(인덱스 안밀림)
        st = st[:pos] + f' {{{{FIG{i}}}}} ' + st[pos:]
    st = re.sub(r'\s*\{\{(FIG\d+)\}\}\s*', r'\n{{\1}}\n', re.sub(r'\s+', ' ', st).strip())
    block = 'searchable_text: |\n' + '\n'.join('  ' + l for l in st.splitlines()) + '\n'
    txt = txt[:m.start() + 1] + block + txt[m.end():]
    txt = re.sub(r'\nfigures:\n(?:  - .*\n)*', '\n', txt)  # 기존 figures 제거
    figblock = '\n'.join(f'  - image: {f["image"]}' for f in figs)
    txt = re.sub(r'(\nproblem_image: .*\n)', r'\1figures:\n' + figblock + '\n', txt, count=1)
    open(md, 'w', encoding='utf-8').write(txt)
    return None


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--apply']
    do_apply = '--apply' in sys.argv
    figs, err = extract(*args[:3])
    if err: print('FAIL:', err); sys.exit(1)
    print(json.dumps(figs, ensure_ascii=False, indent=2))
    if do_apply:
        print('APPLY:', apply_md(*args[:3], figs) or 'OK')
