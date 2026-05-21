#!/usr/bin/env python3
"""Per-problem bbox extraction from KICE/모의고사 PDFs.

PNG-First pipeline: instead of OCR'ing pages and trying to split markdown,
we directly identify each problem's location in the PDF via text-layer
"N." anchors, compute its bounding box (current anchor's y to next anchor's
y in the same column), and crop the rendered page PNG to that region.
The cropped PNG becomes the problem's body — visual ground truth, no OCR.

Subject inference uses canonical_area_for_page (covers 수능/모평/고3 모의고사
공통→확률통계/미적분/기하 split), or falls back to '단일' for 학평/검정고시.

Returns: list of dicts:
    { 'subject': str, 'number': int, 'page_num': int,
      'bbox_pdf': (x0, y0, x1, y1) in PDF points,
      'bbox_px':  (x0, y0, x1, y1) in image pixels at DPI }
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

_SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(_SCRIPTS))
try:
    from ocr_client import _canonical_area_for_page  # type: ignore
except Exception:
    _canonical_area_for_page = lambda p, n: None  # noqa: E731


# Two-column layout — column geometry is fixed relative to page width.
# KICE PDFs ship at two scales: 595×841 (A4 points) and 841×1191 (larger
# render). All ratios below are page-width fractions so both work.
LEFT_MARGIN_RATIO = 0.05    # left page margin
RIGHT_MARGIN_RATIO = 0.95   # right page margin
MIDLINE_RATIO = 0.50        # column divider center
COL_OVERLAP_RATIO = 0.085   # left col extends right by this much to
                            # capture choice rows whose last item
                            # (e.g. ⑤) drifts past the midline
BBOX_PAD_PT = 6.0
PAGE_TOP_MARGIN_PT = 50.0
PAGE_BOTTOM_MARGIN_PT = 50.0


def _detect_layout(pdf_path: Path) -> dict[str, float]:
    """Sample the PDF's text-layer to detect actual column boundaries
    instead of assuming page-width × 0.50. KICE A4 PDFs follow that, but
    검정고시 (729×1032) and some 학평 (612×790) use different ratios.

    Returns {'mid', 'left_min', 'right_max', 'overlap', 'page_w'} in PDF
    points. Mid is the column divider; overlap is how far the left column
    extends past mid to capture choice rows that drift right.
    """
    try:
        d = fitz.open(pdf_path)
    except Exception:
        return {'mid': 297.5, 'left_min': 30, 'right_max': 560, 'overlap': 50, 'page_w': 595}
    page_w = d[0].rect.width
    # Sample anchor x-positions (where "N." line-starts sit) — these
    # cluster tightly at the two column starts and ignore body/choice noise.
    anchor_xs: list[float] = []
    body_x_ends: list[float] = []
    for page in d:
        text_dict = page.get_text('dict')
        for block in text_dict.get('blocks', []):
            if block.get('type', 0) != 0:
                continue
            for line in block.get('lines', []):
                spans = line.get('spans', [])
                if not spans:
                    continue
                first = spans[0].get('text', '').strip()
                if re.match(r'^\d{1,2}\.\s*', first):
                    anchor_xs.append(line['bbox'][0])
                body_x_ends.append(line['bbox'][2])
    d.close()
    if not anchor_xs:
        # Fallback: page-width × 0.50
        mid = page_w * 0.50
        return {'mid': mid, 'left_min': page_w * 0.05,
                'right_max': page_w * 0.95, 'overlap': page_w * 0.08, 'page_w': page_w}

    # Anchors form two tight clusters: left-column starts (~62pt) and
    # right-column starts (~333pt for 595-wide pages, scaled for others).
    # Find the largest gap in the sorted anchor xs — that's the divider.
    sorted_xs = sorted(anchor_xs)
    if len(sorted_xs) < 2:
        mid = page_w * 0.50
        return {'mid': mid, 'left_min': page_w * 0.05,
                'right_max': page_w * 0.95, 'overlap': page_w * 0.08, 'page_w': page_w}
    biggest_gap = 0.0
    split_at = -1
    for i in range(len(sorted_xs) - 1):
        g = sorted_xs[i + 1] - sorted_xs[i]
        if g > biggest_gap:
            biggest_gap = g
            split_at = i
    # Single-column PDF: no big gap means all anchors at one x
    if biggest_gap < 50:
        left_min = max(0, sorted_xs[0] - 15)
        right_max = min(page_w, max(body_x_ends) + 15) if body_x_ends else page_w * 0.95
        return {'mid': page_w * 0.99, 'left_min': left_min,
                'right_max': right_max, 'overlap': 0, 'page_w': page_w}

    # mid = right column's anchor start (where right-column content
    # begins). This is the actual boundary downstream code uses to split
    # anchors. left column extends past mid by overlap_pt to capture wide
    # choice rows where ⑤ drifts right.
    left_max_anchor = sorted_xs[split_at]
    right_min_anchor = sorted_xs[split_at + 1]
    # Classification midline: midpoint between the two column anchor
    # clusters so `x > classify_mid` cleanly separates them. Using
    # right_min_anchor itself fails when the right column's anchor x
    # equals it exactly (e.g. 285.6 > 285.6 is False → wrong column).
    classify_mid = (left_max_anchor + right_min_anchor) / 2.0
    # mid (the rect boundary) is the right column's anchor start —
    # left rect ends a little past it via overlap, right rect starts there.
    mid = right_min_anchor
    # Overlap: enough to catch ⑤ at the end of a choice row, but never
    # so much that it swallows the right column's anchor.
    overlap = min((right_min_anchor - left_max_anchor) * 0.50, page_w * 0.10)
    left_anchor_min = sorted_xs[0]
    left_min = max(0, left_anchor_min - 15)
    right_max = min(page_w, max(body_x_ends) + 15) if body_x_ends else page_w * 0.95
    return {'mid': mid, 'classify_mid': classify_mid, 'left_min': left_min,
            'right_max': right_max, 'overlap': overlap, 'page_w': page_w}


def _column_bounds(layout: dict[str, float], col_idx: int) -> tuple[float, float]:
    """Return (x0, x1) for the column based on detected layout.

    `mid` is the right column's anchor start (where right-column content
    begins). Left column ends just before mid. The 3pt safety gap keeps
    right-column "N." anchors out of the left column rect. We do NOT add
    any overlap into the right column — overlap was used to catch
    ⑤ that drifts past the divider, but in practice it pulled in the
    right column's body and confused the LLM's y_ratio decision.
    """
    SAFETY_GAP_PT = 3.0
    if col_idx == 0:
        return (layout['left_min'], layout['mid'] - SAFETY_GAP_PT)
    return (layout['mid'], layout['right_max'])


def _detect_footer_top(page: fitz.Page) -> float:
    """Per-page footer/page-number top y-coordinate.

    KICE A4 PDFs put the page number ~30pt above page bottom;
    EBSi 모의고사 (larger pages) put it ~85-90pt above bottom inside a
    rounded box. A fixed PAGE_BOTTOM_MARGIN_PT can't cover both. We look
    for a short numeric token (the page number) in the bottom 150pt and
    use its top y as the footer line. Fallback = page_h - 50pt.

    Returns the y above which all problem content must stay.
    """
    h = page.rect.height
    footer_candidates: list[float] = []
    for w in page.get_text('words'):
        x0, y0, x1, y1, txt, *_ = w
        if y0 > h - 150 and re.match(r'^\d{1,3}$', txt.strip()):
            footer_candidates.append(y0)
    if footer_candidates:
        # 5pt safety above the page number box
        return min(footer_candidates) - 5.0
    return h - PAGE_BOTTOM_MARGIN_PT


def _find_problem_anchors(page: fitz.Page) -> list[tuple[int, float, float]]:
    """Return [(number, x_start, y_start)] for "N." line starts on the page.
    Uses dict-mode text extraction so we get bbox coords per line.

    PyMuPDF sometimes splits "27." into two spans ("27" + "."). We therefore
    concatenate the first few spans before matching, and accept the line as
    an anchor only if the combined leading text starts with `\\d{1,2}\\.`.
    """
    out: list[tuple[int, float, float]] = []
    text_dict = page.get_text('dict')
    for block in text_dict.get('blocks', []):
        if block.get('type', 0) != 0:
            continue
        for line in block.get('lines', []):
            spans = line.get('spans', [])
            if not spans:
                continue
            # Join the first 3 spans — enough for "27", ".", " 함수" patterns.
            leading = ''.join(s.get('text', '') for s in spans[:3]).lstrip()
            m = re.match(r'^(\d{1,2})\.\s*', leading)
            if not m:
                continue
            n = int(m.group(1))
            if not (1 <= n <= 50):
                continue
            x0, y0, _, _ = line['bbox']
            out.append((n, x0, y0))
    return out


def _collect_text_lines(page: fitz.Page) -> list[tuple[float, float, float, float]]:
    """Return every meaningful text line's bbox. Skip only the page-footer
    area (bottom 60pt) so the boxed page number doesn't drag y_end down.
    Length-based filtering was tried but it discards legitimate single-
    character lines like the answer choices "① 3  ② 4  ③ 5  ④ 6" that
    PyMuPDF sometimes splits per token — losing those clips the bottom
    of multiple-choice problems."""
    out: list[tuple[float, float, float, float]] = []
    page_height = page.rect.height
    footer_y = page_height - 60.0
    text_dict = page.get_text('dict')
    for block in text_dict.get('blocks', []):
        if block.get('type', 0) != 0:
            continue
        for line in block.get('lines', []):
            bbox = line.get('bbox')
            if not bbox:
                continue
            # Skip page footer only
            if bbox[1] >= footer_y:
                continue
            out.append(bbox)
    return out


def _column_of(x: float, mid: float = 297.5) -> int:
    """0 = left column, 1 = right column. Pass the layout's detected
    `mid` (from _detect_layout) for accurate split on non-standard PDFs."""
    return 1 if x > mid else 0


def _classify_subject(canonical_area: str | None, exam_type: str, grade: str | None,
                      number: int) -> str:
    """Subject for this problem.
    - If PDF page declares an elective area (확률통계/미적분/기하), trust it.
    - 수능/모평/고3 모의고사·학평: 1-22 are 공통, 23-30 fall under the page's elective.
      Numbers 23-30 on a page WITHOUT an elective header are still 공통 (e.g. 학평 단일형).
    - 학평/모의고사 고1·고2, 검정고시: always 단일.
    """
    if exam_type in ('모의고사', '학력평가') and grade in ('고1', '고2'):
        return '단일'
    if exam_type == '검정고시':
        return '단일'
    # 수능/모평/고3 모의고사 layout
    if canonical_area:  # PDF says (확률과 통계) / (미적분) / (기하)
        return canonical_area
    return '공통'


def extract_problem_bboxes(pdf_path: Path, exam_type: str, grade: str | None,
                           dpi: int = 200) -> list[dict]:
    """Top-level entry. Walk every page, find "N." anchors, group by column,
    and compute each problem's vertical extent (this anchor → next anchor
    in same page+column, or page bottom).

    Returns a list ordered by (subject, number). Duplicate (subject, number)
    can occur if the same problem appears split across pages — caller can
    merge or pick the larger.
    """
    d = fitz.open(pdf_path)
    raw_entries: list[dict] = []
    # First pass: collect anchors + page metadata
    pages_data: list[dict] = []
    for i, page in enumerate(d):
        anchors = _find_problem_anchors(page)
        canonical_area = _canonical_area_for_page(pdf_path, i + 1)
        footer_top = _detect_footer_top(page)
        pages_data.append({
            'page_num': i + 1,
            'page_rect': page.rect,
            'anchors': anchors,
            'canonical_area': canonical_area,
            'footer_top': footer_top,
        })

    # Cache page → text lines (avoid re-parsing each anchor)
    page_lines_cache: dict[int, list[tuple[float, float, float, float]]] = {}
    d2 = fitz.open(pdf_path)
    for i in range(d2.page_count):
        page_lines_cache[i + 1] = _collect_text_lines(d2[i])
    d2.close()

    # Detect column layout for this PDF (mid / overlap / left_min / right_max)
    layout = _detect_layout(pdf_path)
    # classify_mid is the strict left/right boundary for anchors; mid is the
    # rect-boundary used for crop widths. They differ when columns are not
    # symmetric (left_max_anchor=58, right_min_anchor=285 → classify_mid=171.7).
    classify_mid = layout.get('classify_mid', layout['mid'])

    for pd in pages_data:
        page_num = pd['page_num']
        rect = pd['page_rect']
        anchors = pd['anchors']
        canonical_area = pd['canonical_area']
        footer_top = pd['footer_top']
        if not anchors:
            continue
        # Group anchors by column using the PDF-specific detected midline.
        cols: dict[int, list[tuple[int, float, float]]] = {0: [], 1: []}
        for n, x, y in anchors:
            cols[_column_of(x, classify_mid)].append((n, x, y))
        for col_idx, col_anchors in cols.items():
            if not col_anchors:
                continue
            col_anchors.sort(key=lambda t: t[2])
            col_x0, col_x1 = _column_bounds(layout, col_idx)
            for idx, (n, x, y) in enumerate(col_anchors):
                # Generous hard upper bound: next anchor in same column or
                # column bottom. The actual end (so the cropped PNG doesn't
                # carry empty whitespace) is decided downstream by
                # `crop_with_llm`, which can SEE the problem and the empty
                # space below it. The algorithm only needs to guarantee
                # the candidate region INCLUDES the full problem (incl.
                # figure + last 보기 row); over-inclusion is fine because
                # the LLM trims.
                if idx + 1 < len(col_anchors):
                    hard_end = col_anchors[idx + 1][2] - BBOX_PAD_PT
                else:
                    # Last problem in this column on this page — stop at
                    # the detected footer line (page number box) instead
                    # of a fixed bottom margin.
                    hard_end = footer_top
                # Never let hard_end go past the footer even when next
                # anchor is further down (rare but defensive).
                hard_end = min(hard_end, footer_top)
                y_start = max(PAGE_TOP_MARGIN_PT, y - BBOX_PAD_PT)
                y_end = hard_end
                bbox_pdf = (col_x0, y_start, col_x1, y_end)
                subject = _classify_subject(canonical_area, exam_type, grade, n)
                raw_entries.append({
                    'subject': subject,
                    'number': n,
                    'page_num': page_num,
                    'bbox_pdf': bbox_pdf,
                    'bbox_px': _pdf_to_pixels(bbox_pdf, dpi),
                })

    d.close()
    # Sort by (subject, number, page) — earliest page first.
    # KICE 수능 PDFs ship 홀수형(p1-20) + 짝수형(p21-40) together; we want
    # only one copy per problem and 홀수형 (the first occurrence) is what
    # the answer table in our extract_answers pipeline aligns with.
    raw_entries.sort(key=lambda e: (e['subject'], e['number'], e['page_num']))
    deduped: list[dict] = []
    seen: set[tuple[str, int]] = set()
    for e in raw_entries:
        key = (e['subject'], e['number'])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)
    return deduped


def _pdf_to_pixels(bbox_pdf: tuple[float, float, float, float], dpi: int) -> tuple[int, int, int, int]:
    """Convert PDF points to image pixels at given DPI. 1 inch = 72 pt."""
    scale = dpi / 72.0
    x0, y0, x1, y1 = bbox_pdf
    return (int(x0 * scale), int(y0 * scale),
            int(x1 * scale), int(y1 * scale))


def crop_problem_image(page_png: Path, bbox_px: tuple[int, int, int, int],
                       output_path: Path) -> Path:
    """Crop the bbox region from a rendered page PNG, then content-trim:
    the bbox covers the full column until the next problem's anchor, so for
    short problems most of that area is whitespace. PIL.getbbox() finds the
    actual ink region after inversion; we crop to that + small padding.
    Result: tight image around the real problem content (text + figure +
    choices), no big blank tail."""
    from PIL import ImageOps, ImageChops, Image as PILImage
    BBOX_PAD_PX = 8
    TRIM_PAD_PX = 12  # breathing room around content after trim
    img = Image.open(page_png)
    w, h = img.size
    x0, y0, x1, y1 = bbox_px
    x0 = max(0, x0 - BBOX_PAD_PX)
    y0 = max(0, y0 - BBOX_PAD_PX)
    x1 = min(w, x1 + BBOX_PAD_PX)
    y1 = min(h, y1 + BBOX_PAD_PX)
    cropped = img.crop((x0, y0, x1, y1))

    # Content-aware trim: detect non-background (non-white) region.
    # Grayscale → diff from white (255) → bbox of non-zero pixels = ink region.
    gray = cropped.convert('L')
    bg = PILImage.new('L', gray.size, 255)
    diff = ImageChops.difference(gray, bg)
    # Threshold tiny noise (anti-aliasing): treat <12 as background
    diff = diff.point(lambda v: 255 if v > 12 else 0)
    ink_bbox = diff.getbbox()
    if ink_bbox:
        ix0, iy0, ix1, iy1 = ink_bbox
        cw, ch = cropped.size
        ix0 = max(0, ix0 - TRIM_PAD_PX)
        iy0 = max(0, iy0 - TRIM_PAD_PX)
        ix1 = min(cw, ix1 + TRIM_PAD_PX)
        iy1 = min(ch, iy1 + TRIM_PAD_PX)
        cropped = cropped.crop((ix0, iy0, ix1, iy1))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_path, 'PNG', optimize=True)
    return output_path


def crop_problem_image_multipage(page_pngs: list[Path], bboxes_px: list[tuple[int, int, int, int]],
                                  output_path: Path) -> Path:
    """For a problem that spans multiple pages: vertically stack the crops
    so the visual remains a single contiguous image."""
    if len(page_pngs) == 1:
        return crop_problem_image(page_pngs[0], bboxes_px[0], output_path)
    BBOX_PAD_PX = 8
    crops = []
    max_w = 0
    total_h = 0
    for png, bbox in zip(page_pngs, bboxes_px):
        img = Image.open(png)
        w, h = img.size
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0 - BBOX_PAD_PX); y0 = max(0, y0 - BBOX_PAD_PX)
        x1 = min(w, x1 + BBOX_PAD_PX); y1 = min(h, y1 + BBOX_PAD_PX)
        c = img.crop((x0, y0, x1, y1))
        crops.append(c)
        max_w = max(max_w, c.width)
        total_h += c.height
    stacked = Image.new('RGB', (max_w, total_h), 'white')
    y_cursor = 0
    for c in crops:
        stacked.paste(c, (0, y_cursor))
        y_cursor += c.height
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stacked.save(output_path, 'PNG', optimize=True)
    return output_path


if __name__ == '__main__':
    # Smoke test: 2026 고1 3월
    import sys
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('db/raw/2026_고1_3월모의고사/문제.pdf')
    entries = extract_problem_bboxes(pdf, exam_type='모의고사', grade='고1')
    print(f'{pdf}: {len(entries)} problems detected')
    for e in entries[:5]:
        print(f'  {e["subject"]:>5s} #{e["number"]:>2d}  p{e["page_num"]}  '
              f'bbox_pt=({e["bbox_pdf"][0]:.0f},{e["bbox_pdf"][1]:.0f},{e["bbox_pdf"][2]:.0f},{e["bbox_pdf"][3]:.0f})')
    print(f'  ... ({len(entries) - 5} more)' if len(entries) > 5 else '')
