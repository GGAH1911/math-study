r"""기출 PDF 도형 추출 파이프라인.

한컴 출신 기출 PDF는 도형/그래프를 **임베드 이미지 오브젝트(고해상도 JPEG, ~400DPI)**로
저장한다(일부 회차는 벡터). 페이지를 다시 렌더해 크롭하는 대신, 그 오브젝트를 직접 뽑으면
네이티브 해상도·정확한 경계로 얻는다. HWP 내보내기가 한 도형을 가로 스트립 여러 장으로
쪼개므로 bbox 인접성으로 stitch하고, bbox.py 문제 영역과 매칭해 문제별 도형 PNG를 만든다.

좌표계: pdfminer=bottom-left, bbox.py=top-left(같은 포인트 스케일). 변환: top_y = H - btm_y.
"""
from __future__ import annotations
import os
from collections import defaultdict
import pikepdf
from PIL import Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage
from bbox import extract_problem_bboxes


def _ltimages(pdf):
    out = defaultdict(list); dims = {}
    for pi, page in enumerate(extract_pages(pdf)):
        dims[pi] = (page.width, page.height)
        def walk(el):
            if isinstance(el, LTImage):
                out[pi].append([el.name, tuple(el.bbox), el.srcsize])
            if hasattr(el, '__iter__'):
                for c in el:
                    walk(c)
        walk(page)
    return out, dims


def _pils(pdf):
    out = defaultdict(dict); p = pikepdf.open(pdf)
    for pi, page in enumerate(p.pages):
        for name, raw in page.images.items():
            try:
                out[pi][name.lstrip('/')] = pikepdf.PdfImage(raw).as_pil_image()
            except Exception:
                pass
    return out


def _group(imgs):
    """같은 x-range·세로 인접한 이미지들을 한 도형으로 묶음(union)."""
    used = [False] * len(imgs); groups = []
    for i in range(len(imgs)):
        if used[i]:
            continue
        gi = [i]; used[i] = True; ch = True
        while ch:
            ch = False
            gx0 = min(imgs[k][1][0] for k in gi); gx1 = max(imgs[k][1][2] for k in gi)
            gy0 = min(imgs[k][1][1] for k in gi); gy1 = max(imgs[k][1][3] for k in gi)
            for j in range(len(imgs)):
                if used[j]:
                    continue
                x0, y0, x1, y1 = imgs[j][1]
                xov = min(gx1, x1) - max(gx0, x0); xmin = min(gx1 - gx0, x1 - x0)
                yov = min(gy1, y1) - max(gy0, y0); ygap = max(gy0 - y1, y0 - gy1)
                if xov > 0.4 * xmin and (yov > -3 or ygap < 8):
                    gi.append(j); used[j] = True; ch = True
        groups.append(gi)
    return groups


def _stitch(gimgs, pils):
    gx0 = min(b[1][0] for b in gimgs); gx1 = max(b[1][2] for b in gimgs)
    gy0 = min(b[1][1] for b in gimgs); gy1 = max(b[1][3] for b in gimgs)
    avail = [b for b in gimgs if b[0] in pils]
    if not avail:
        return None, (gx0, gy0, gx1, gy1)
    scale = max(pils[b[0]].width / max(1, (b[1][2] - b[1][0])) for b in avail)
    W = max(1, round((gx1 - gx0) * scale)); H = max(1, round((gy1 - gy0) * scale))
    canvas = Image.new('RGB', (W, H), 'white')
    for name, bb, ss in gimgs:
        if name not in pils:
            continue
        w = max(1, round((bb[2] - bb[0]) * scale)); h = max(1, round((bb[3] - bb[1]) * scale))
        im = pils[name].resize((w, h))
        canvas.paste(im, (round((bb[0] - gx0) * scale), round((gy1 - bb[3]) * scale)))
    return canvas, (gx0, gy0, gx1, gy1)


def extract_figures(pdf):
    """[{page, bbox(pdfminer btm-left), image(PIL), strips, page_dims}]. 전면 이미지 제외."""
    lti, dims = _ltimages(pdf); pil = _pils(pdf); figs = []
    for pi in sorted(lti):
        pw, ph = dims[pi]
        for g in _group(lti[pi]):
            gimgs = [lti[pi][k] for k in g]
            canvas, bb = _stitch(gimgs, pil.get(pi, {}))
            if canvas is None:
                continue
            area = (bb[2] - bb[0]) * (bb[3] - bb[1])
            if area > 0.6 * pw * ph:  # 전면/배경 이미지(답안지 등) 제외
                continue
            figs.append({'page': pi, 'bbox': bb, 'image': canvas, 'strips': len(g), 'page_dims': (pw, ph)})
    return figs


def map_to_problems(pdf, exam_type='모의고사', grade='고3'):
    """[{problem(int|None), page, bbox, image, strips}] — 도형↔문제 매칭."""
    figs = extract_figures(pdf)
    ents = extract_problem_bboxes(pdf, exam_type=exam_type, grade=grade)
    by_page = defaultdict(list)
    for e in ents:
        by_page[e['page_num']].append(e)
    out = []
    for f in figs:
        pw, ph = f['page_dims']; bb = f['bbox']
        cx = (bb[0] + bb[2]) / 2; cy = ph - (bb[1] + bb[3]) / 2  # top-left center
        best = None
        for e in by_page.get(f['page'] + 1, []):  # bbox.py page_num = pdfminer+1
            x0, y0, x1, y1 = e['bbox_pdf']
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                best = e; break
        out.append({'problem': best['number'] if best else None,
                    'subject': best['subject'] if best else None, 'page': f['page'],
                    'bbox': bb, 'image': f['image'], 'strips': f['strips']})
    return out


def render_region(pdf, page_num, clip_bbox, dpi=300):
    """벡터 도형 폴백: 문제(또는 도형) 영역을 고DPI로 렌더(벡터라 어떤 해상도도 선명).

    page_num=bbox.py 1-index, clip_bbox=fitz top-left 포인트(=bbox.py bbox_pdf와 동일계).
    """
    import io
    import fitz
    doc = fitz.open(pdf)
    page = doc[page_num - 1]
    pix = page.get_pixmap(clip=fitz.Rect(*clip_bbox), dpi=dpi)
    return Image.open(io.BytesIO(pix.tobytes('png')))


def recompute_has_figure(pdf, exam_type='모의고사', grade='고3'):
    """이미지 추출 = 진실로 has_figure 재계산.

    반환 {problem_number: {'has_figure':bool,'type':'image','strips':int,'bbox':...}}.
    여기엔 임베드 이미지 도형만 확정. 벡터/표/없음 구분은 호출측에서 영역 렌더+비전으로
    최종 판정(기존 has_figure 메타가 양방향 오류라 신뢰 불가).
    """
    out = {}
    for m in map_to_problems(pdf, exam_type, grade):
        if m['problem'] is None:
            continue
        out[m['problem']] = {'has_figure': True, 'type': 'image',
                             'strips': m['strips'], 'bbox': m['bbox']}
    return out


def save_problem_figures(pdf, outdir, prefix, exam_type='모의고사', grade='고3'):
    """문제별 도형 PNG 저장. 반환: {problem_number: filepath}."""
    os.makedirs(outdir, exist_ok=True); saved = {}
    for m in map_to_problems(pdf, exam_type, grade):
        if m['problem'] is None:
            continue
        fp = os.path.join(outdir, f'{prefix}_{m["problem"]}_fig.png')
        m['image'].save(fp); saved[m['problem']] = fp
    return saved


if __name__ == '__main__':
    import sys
    for m in map_to_problems(sys.argv[1]):
        print(f"  문제 {str(m['problem']):>4}  ← page{m['page']} 조각{m['strips']}개 {m['image'].size}px")
