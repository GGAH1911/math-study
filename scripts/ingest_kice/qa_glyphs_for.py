#!/usr/bin/env python3
"""문제 ID의 글리프(decode_str, x/y/size)를 decode_pdf와 동일 추출로 덤프. 결정론 신호 분석용.
usage: python3 glyphs_for.py <id> [필터문자]
  id 예: 2022/고1_6월모의고사/2022_고1_6월모의고사_단일_03"""
import sys
sys.path.insert(0, 'scripts/ingest_kice')
import hancom_decode as H
import backfill_rosetta as B
from bbox import extract_problem_bboxes
from pdfminer.high_level import extract_pages

pid = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else None
md = B.parse_md('docs/problems/' + pid + '.md')
pdf = B.pdf_for(md)
pages = {}
for pi, page in enumerate(extract_pages(pdf)):
    chars, bars = H._page_chars_bars(page)
    pages[pi] = (page.height, chars, bars)
e = None
for et in (md['exam_type'], '수능', '모의고사', '모의평가', '학력평가'):
    try:
        ents = extract_problem_bboxes(pdf, exam_type=et or '수능', grade=md['grade'] or '고3')
    except Exception:
        continue
    cand = [x for x in ents if x['number'] == md['num'] and x['subject'] == md['subject']] \
        or [x for x in ents if x['number'] == md['num']]
    if cand:
        e = cand[0]
        break
Hh, chars, bars = pages[e['page_num'] - 1]
bx0, by0, bx1, by1 = e['bbox_pdf']
rc = [c for c in chars if bx0 - 2 <= (c.x0 + c.x1) / 2 <= bx1 + 2 and by0 - 2 <= (Hh - (c.y0 + c.y1) / 2) <= by1 + 2]
rb = [b for b in bars if bx0 - 2 <= (b[0] + b[1]) / 2 <= bx1 + 2 and by0 - 2 <= (Hh - b[2]) <= by1 + 2]
print('DECODE:', H._parse(rc, rb))
print(f'--- glyphs: {len(rc)}개, 괘선 {len(rb)}개 (y desc, x asc) ---')
for c in sorted(rc, key=lambda c: (round(-(c.y0 + c.y1) / 2, 1), c.x0)):
    s = H.decode_str(c.get_text())
    if pat and pat not in s:
        continue
    print(f'{s!r:8} x{c.x0:7.1f}-{c.x1:7.1f} yc{(c.y0 + c.y1) / 2:7.1f} sz{c.size:4.1f}')
