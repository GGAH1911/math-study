#!/usr/bin/env python3
"""상단 잘림(위첨자 클립) 보정 — gap-aware 재크롭. 크레딧 0 (순수 PIL + PDF 파싱).

완전성 우선: 첫 줄에서 위로 스캔해 작은 갭(위첨자)은 포함, 큰 갭(문제 사이)에서 정지.
페이지 헤더가 딸려와도 OK(문제 온전성 우선). 안 잘린 문제엔 사실상 no-op.
원본 페이지 렌더(pages/)에서 재크롭 → 사용자 이미지(db/raw/.../images, web symlink) 교체.

사용: python recrop_top.py --numbers 1[,2,3]   |   --list slug1,slug2   [--dry]
"""
from __future__ import annotations
import sys, re, glob, argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts' / 'ingest_kice'))
import crop_with_llm as CW       # noqa: E402
import ingest_v2 as IV           # noqa: E402

BLANK = CW.BLANK_ROW_INK_RATIO
_bbox_cache: dict = {}


def gap_aware(page_img: Image.Image, bbox_px, out_path: Path, exam_type, gen=90, big_gap=30):
    x0, y0, x1, y1 = bbox_px
    top = max(0, y0 - gen)
    cand = page_img.crop((x0, top, x1, y1))
    ri = CW._row_ink_ratios(cand.convert('L'))
    anchor = y0 - top
    n = len(ri)
    sl = next((y for y in range(max(0, anchor - 3), n) if ri[y] >= BLANK), anchor)
    ty, bl, y = sl, 0, sl - 1
    while y >= 0:
        if ri[y] >= BLANK:
            ty = y; bl = 0
        else:
            bl += 1
            if bl >= big_gap:
                break                                # 큰 갭 → 정지(문제 사이)
        y -= 1
    clean = cand.crop((0, max(0, ty - 2), cand.width, cand.height))
    tmp = ROOT / 'db' / 'raw' / '.recrop_tmp.png'
    clean.save(tmp)
    CW.crop_by_gap(tmp, out_path, exam_type=exam_type)
    tmp.unlink(missing_ok=True)


def _round_entries(round_slug, exam_type, session, subject):
    """회차 bbox 캐시. PDF: 문제.pdf 또는 <subject>_문제.pdf(ganah 가/나형)."""
    key = round_slug
    if key in _bbox_cache:
        return _bbox_cache[key]
    raw = ROOT / 'db' / 'raw' / round_slug
    pdf = raw / '문제.pdf'
    if not pdf.exists() and subject in ('가형', '나형'):
        pdf = raw / f'{subject}_문제.pdf'
    if not pdf.exists():
        _bbox_cache[key] = None; return None
    pages_dir = raw / 'pages'
    if not list(pages_dir.glob('*.png')):
        IV.render_pdf_pages(pdf, pages_dir)
    page_by_num = {int(p.stem[1:]): p for p in pages_dir.glob('*.png')}
    et = '모의평가' if exam_type in ('모평', '모의평가') else exam_type
    ents = IV.extract_problem_bboxes(pdf, et, session)
    _bbox_cache[key] = (ents, page_by_num)
    return _bbox_cache[key]


def recrop_slug(slug, md_text, dry=False):
    def f(k, d=None):
        m = re.search(rf'^\s*{k}:\s*(.+)$', md_text, re.M)
        return m.group(1).strip().strip('"\'') if m else d
    img_rel = (re.search(r'image_paths:\s*\[([^\]\n]+)', md_text) or [None, None])[1]
    if not img_rel:
        return 'no-img-path'
    img_fs = ROOT / img_rel.split(',')[0].strip()
    round_slug = img_rel.split('/')[2]               # db/raw/<ROUND>/images/...
    exam_type, session = f('exam_type'), f('session')
    subject, number = f('subject'), int(f('number', '0'))
    got = _round_entries(round_slug, exam_type, session, subject)
    if not got:
        return 'no-pdf'
    ents, page_by_num = got
    cands = [e for e in ents if e['number'] == number and
             (subject not in ('가형', '나형') or e.get('subject') == subject)]
    if not cands:
        return 'no-bbox'
    e = cands[0]
    page = page_by_num.get(e['page_num'])
    if not page:
        return 'no-page'
    before = Image.open(img_fs).size if img_fs.exists() else None
    if not dry:
        gap_aware(Image.open(page), e['bbox_px'], img_fs, '모의고사' if exam_type == '모의고사' else exam_type)
    after = Image.open(img_fs).size if img_fs.exists() else None
    return f'ok {before}→{after}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--numbers', help='쉼표구분 문제번호 (예: 1 또는 1,2,3)')
    ap.add_argument('--list', help='쉼표구분 slug')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    md_by = {p.split('/')[-1][:-3]: p for p in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)}
    if a.list:
        slugs = [s.strip() for s in a.list.split(',') if s.strip()]
    elif a.numbers:
        nums = set(a.numbers.split(','))
        slugs = [s for s in md_by if s.rsplit('_', 1)[-1] in {n.zfill(2) for n in nums}]
    else:
        print('--numbers 또는 --list 필요'); return
    print(f"대상 {len(slugs)}개 (dry={a.dry})", flush=True)
    from collections import Counter
    res = Counter()
    for i, s in enumerate(sorted(slugs), 1):
        try:
            r = recrop_slug(s, open(md_by[s]).read(), a.dry)
        except Exception as ex:
            r = f'err:{ex}'
        tag = r.split()[0]
        res[tag] += 1
        if tag != 'ok' or i <= 5:
            print(f"  [{i}/{len(slugs)}] {s}: {r}", flush=True)
    print(f"\n결과: {dict(res)}", flush=True)


if __name__ == '__main__':
    main()
