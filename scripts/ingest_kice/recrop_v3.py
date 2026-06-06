#!/usr/bin/env python3
"""Crop-only smoke-test — 인제스트와 동일한 crop_problem(원래경계+headroom) 사용.

Runs the cheap part of the v3 ingest pipeline (PDF render + bbox extract +
PIL crop) across every round in db/raw/ — no LLM, no metadata, no DB
upsert. Result: `db/raw/{slug}/images/*.png` + `web/public/problem-images/`
symlinks updated so the /progress preview grid shows the fresh crops.

Typical use: tune crop_with_llm.py knobs (GAP_RATIO, PADDING_RATIO),
run this, eyeball /progress, iterate.
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import sys
import time
from pathlib import Path

import fitz
from PIL import Image

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))

import importlib
import json
import bbox; importlib.reload(bbox)
import crop_with_llm; importlib.reload(crop_with_llm)
from bbox import extract_problem_bboxes  # noqa: E402
from crop_with_llm import crop_problem  # noqa: E402  (인제스트와 동일 크롭: 원래경계+headroom)
from ingest_v2 import _ensure_web_symlink, ROOT  # noqa: E402
from ingest_round import download, slugify_round  # noqa: E402


def _exam_meta_from_slug(slug: str) -> tuple[str, str | None]:
    """Best-effort (exam_type, grade) inference from slug — only used so
    bbox.extract_problem_bboxes can pick the right canonical_area logic
    (수능/모평/고3 → 공통+선택 split; 학평/검정고시 → 단일)."""
    if '_수능' in slug:
        return '수능', None
    if '_예시' in slug:
        return '수능', None
    if '월모평' in slug:
        return '모의평가', None
    if '_고1_' in slug:
        return '모의고사', '고1'
    if '_고2_' in slug:
        return '모의고사', '고2'
    if '_고3_' in slug:
        return '모의고사', '고3'
    if '_중졸_' in slug:
        return '검정고시', '중졸'
    if '_고졸_' in slug:
        return '검정고시', '고졸'
    return '모의고사', None


def _render_pages_if_missing(pdf: Path, pages_dir: Path, dpi: int = 200) -> int:
    """Render p*.png at `dpi` if any are missing, truncated, or rendered at
    a different DPI than requested.

    A 0-byte (or <1KB) PNG from a failed earlier run is treated as
    missing — PIL would crash with 'cannot identify image file' on it.
    To stay simple we wipe and re-render the whole pages_dir whenever
    we detect any bad/missing file, or a DPI change (page width mismatch).
    """
    pages_dir.mkdir(parents=True, exist_ok=True)
    d = fitz.open(pdf)
    expected = d.page_count
    existing = sorted(pages_dir.glob('p*.png'))
    healthy = [p for p in existing if p.stat().st_size > 1024]
    # DPI 일치 확인: 기존 페이지 폭이 현재 dpi 기대폭과 다르면 재렌더(bbox와 DPI 일치 필수).
    dpi_match = True
    if healthy:
        exp_w = round(d[0].rect.width * dpi / 72.0)
        try:
            dpi_match = abs(Image.open(healthy[0]).size[0] - exp_w) <= 3
        except Exception:
            dpi_match = False
    if len(healthy) == expected and dpi_match:
        d.close()
        return 0
    # Wipe and re-render — partial set, corrupt files, or DPI changed.
    for f in existing:
        try: f.unlink()
        except Exception: pass
    n = 0
    for i, p in enumerate(d):
        p.get_pixmap(dpi=dpi).save(pages_dir / f'p{i+1:02d}.png')
        n += 1
    d.close()
    return n


def recrop_round(slug: str, workers: int = 4, wipe: bool = False, dpi: int = 200) -> dict:
    raw = ROOT / 'db' / 'raw' / slug
    pdf = raw / '문제.pdf'
    pages_dir = raw / 'pages'
    images_dir = raw / 'images'
    if not pdf.exists():
        return {'slug': slug, 'skipped': 'no pdf'}

    if wipe and images_dir.exists():
        # Drop stale images + their web symlinks so leftover crops from
        # an earlier (wrong-bbox) run don't survive.
        web_dir = ROOT / 'web' / 'public' / 'problem-images'
        for f in images_dir.glob('*.png'):
            try: f.unlink()
            except Exception: pass
        for f in images_dir.glob('.cand_*.png'):
            try: f.unlink()
            except Exception: pass
        if web_dir.exists():
            for f in web_dir.glob(f'{slug}_*.png'):
                try: f.unlink()
                except Exception: pass

    exam_type, grade = _exam_meta_from_slug(slug)

    rendered = _render_pages_if_missing(pdf, pages_dir, dpi=dpi)
    entries = extract_problem_bboxes(pdf, exam_type=exam_type, grade=grade, dpi=dpi)
    if not entries:
        return {'slug': slug, 'skipped': 'no bboxes'}

    images_dir.mkdir(parents=True, exist_ok=True)
    page_png_by_num = {int(p.stem[1:]): p for p in pages_dir.glob('p*.png')}

    def _process_one(e):
        page_png = page_png_by_num.get(e['page_num'])
        if not page_png:
            return e, False, 'no page'
        img_name = f'{slug}_{e["subject"]}_{e["number"]:02d}.png'
        img_path = images_dir / img_name
        img = Image.open(page_png)
        ok = crop_problem(img, e['bbox_px'], img_path, exam_type=exam_type)
        if not ok:
            # degenerate; save raw candidate so user still sees something
            img.crop(e['bbox_px']).save(img_path)
            _ensure_web_symlink(img_path)
            return e, False, 'degenerate'
        _ensure_web_symlink(img_path)
        return e, True, None

    done = ok_count = fail_count = 0
    t0 = time.time()
    total = len(entries)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for e, ok, reason in ex.map(_process_one, entries):
            done += 1
            if ok:
                ok_count += 1
            else:
                fail_count += 1
                print(f'    ✗ #{e["number"]:>2} {e["subject"]:>8} {reason}', flush=True)

    return {
        'slug': slug,
        'rendered_pages': rendered,
        'total': total,
        'ok': ok_count,
        'fail': fail_count,
        'elapsed_s': round(time.time() - t0, 1),
    }


def _download_missing_pdfs(manifest_path: Path) -> list[str]:
    """For each manifest entry, ensure db/raw/{slug}/문제.pdf exists.
    Returns the slug list of every manifest entry that ended up with a
    usable PDF (i.e. ready for cropping). Entries whose download fails
    are skipped."""
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    ready: list[str] = []
    for e in data:
        slug = slugify_round(e['year'], e['exam_type'], e.get('session'), e.get('grade'))
        raw = ROOT / 'db' / 'raw' / slug
        pdf = raw / '문제.pdf'
        if pdf.exists() and pdf.stat().st_size > 1000:
            ready.append(slug)
            continue
        url = e.get('pdf_url')
        if not url:
            print(f'  ⤳ skip {slug} — no pdf_url in manifest', flush=True)
            continue
        print(f'  ↓ downloading {slug} from {url}', flush=True)
        if download(url, pdf):
            ready.append(slug)
        else:
            print(f'  ✗ download failed for {slug}', flush=True)
    return ready


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rounds', nargs='*', help='Specific round slugs. Default: all under db/raw/')
    ap.add_argument('--manifest', help='JSON manifest path; download any missing PDFs first, then crop all manifest entries')
    ap.add_argument('--workers', type=int, default=4, help='Per-round parallel crops')
    ap.add_argument('--limit', type=int, default=0, help='Cap to first N rounds')
    ap.add_argument('--wipe', action='store_true',
                    help='Delete images/*.png and matching web symlinks before re-cropping each round')
    ap.add_argument('--dpi', type=int, default=200,
                    help='Render/bbox DPI (must match between page render and bbox). '
                         'Bump to 300 for dense killer problems with small subscripts/figures. Default 200.')
    args = ap.parse_args()

    if args.manifest:
        print(f'== Downloading missing PDFs for manifest {args.manifest} ==', flush=True)
        rounds = _download_missing_pdfs(Path(args.manifest))
        print(f'== {len(rounds)} rounds ready for cropping ==', flush=True)
    elif args.rounds:
        rounds = args.rounds
    else:
        rounds = [d.name for d in sorted((ROOT / 'db' / 'raw').iterdir())
                  if d.is_dir() and (d / '문제.pdf').exists()]
    if args.limit:
        rounds = rounds[:args.limit]
    print(f'recrop_v3 (gap-based, no LLM): {len(rounds)} rounds, workers={args.workers}', flush=True)

    t_start = time.time()
    summary = []
    for i, slug in enumerate(rounds, 1):
        print(f'\n══════ [{i}/{len(rounds)}] {slug} ══════', flush=True)
        try:
            r = recrop_round(slug, workers=args.workers, wipe=args.wipe, dpi=args.dpi)
        except Exception as e:
            r = {'slug': slug, 'error': str(e)[:200]}
        summary.append(r)
        if 'elapsed_s' in r:
            extra = f' (+{r["rendered_pages"]} pages rendered)' if r['rendered_pages'] else ''
            print(f'  ✓ {r["ok"]}/{r["total"]} cropped, {r["fail"]} fail ({r["elapsed_s"]}s){extra}', flush=True)
        elif 'error' in r:
            print(f'  ✗ ERROR: {r["error"]}', flush=True)
        elif 'skipped' in r:
            print(f'  ⤳ skipped: {r["skipped"]}', flush=True)

    print(f'\n══════ Summary ({time.time()-t_start:.0f}s total) ══════')
    total_ok = sum(r.get('ok', 0) for r in summary)
    total_fail = sum(r.get('fail', 0) for r in summary)
    total_total = sum(r.get('total', 0) for r in summary)
    n_skipped = sum(1 for r in summary if 'skipped' in r)
    n_error = sum(1 for r in summary if 'error' in r)
    print(f'  {total_ok}/{total_total} crops ok · {total_fail} fail · {n_skipped} rounds skipped · {n_error} rounds errored')


if __name__ == '__main__':
    main()
