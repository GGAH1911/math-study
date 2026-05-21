#!/usr/bin/env python3
"""Re-crop every problem PNG using the new algorithm-+-LLM pipeline.

Reuses cached pages/, bbox detection, and (where present) meta_cache/
metadata. Only rewrites db/raw/{slug}/images/*.png and refreshes the
web/public/problem-images/ symlinks. Markdown, DB, and metadata stay
untouched — the only thing changing is the visual crop.

Caching:
- candidate column crop is in-memory only (cheap)
- LLM y_ratio cached in db/raw/{slug}/crop_cache/{subject}_{NN}.json
  by candidate PNG sha1, so re-running this script is near-free.
"""
from __future__ import annotations
import argparse
import sys
import time
import shutil
import concurrent.futures as cf
from pathlib import Path

import fitz
from PIL import Image

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))

import importlib
import bbox; importlib.reload(bbox)
from bbox import extract_problem_bboxes  # noqa: E402
from crop_with_llm import crop_with_llm  # noqa: E402
from ingest_v2 import _ensure_web_symlink, ROOT  # noqa: E402


def _exam_meta_from_slug(slug: str) -> tuple[str, str | None]:
    """Best-effort (exam_type, grade) inference from slug."""
    if '_수능' in slug:
        return '수능', None
    if '_모평' in slug:
        return '모의평가', None
    if '_예시' in slug:
        return '수능', None
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


def recrop_round(slug: str, workers: int = 2) -> dict:
    raw = ROOT / 'db' / 'raw' / slug
    pdf = raw / '문제.pdf'
    pages_dir = raw / 'pages'
    images_dir = raw / 'images'
    crop_cache = raw / 'crop_cache'
    if not pdf.exists():
        return {'slug': slug, 'skipped': 'no pdf'}
    exam_type, grade = _exam_meta_from_slug(slug)

    # Re-render pages if missing
    if not list(pages_dir.glob('p*.png')):
        pages_dir.mkdir(parents=True, exist_ok=True)
        d = fitz.open(pdf)
        for i, p in enumerate(d):
            p.get_pixmap(dpi=200).save(pages_dir / f'p{i+1:02d}.png')
        d.close()

    entries = extract_problem_bboxes(pdf, exam_type=exam_type, grade=grade)
    if not entries:
        return {'slug': slug, 'skipped': 'no bboxes'}

    images_dir.mkdir(parents=True, exist_ok=True)
    page_png_by_num = {int(p.stem[1:]): p
                        for p in pages_dir.glob('p*.png')}

    def _process_one(e):
        page_png = page_png_by_num.get(e['page_num'])
        if not page_png:
            return e, False, 'no page'
        img_name = f'{slug}_{e["subject"]}_{e["number"]:02d}.png'
        img_path = images_dir / img_name
        # candidate crop (in-memory, then temp file for LLM)
        img = Image.open(page_png)
        candidate = img.crop(e['bbox_px'])
        tmp = images_dir / f'.cand_{e["subject"]}_{e["number"]:02d}.png'
        candidate.save(tmp)
        cache_key = f'{e["subject"]}_{e["number"]:02d}'
        try:
            ok = crop_with_llm(tmp, img_path, cache_dir=crop_cache,
                               cache_key=cache_key)
        finally:
            try: tmp.unlink()
            except Exception: pass
        if ok:
            _ensure_web_symlink(img_path)
            return e, True, None
        # Fallback: save candidate as-is
        candidate.save(img_path)
        _ensure_web_symlink(img_path)
        return e, False, 'llm fallback to candidate'

    done = ok_count = fail_count = 0
    t0 = time.time()
    total = len(entries)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for e, ok, reason in ex.map(_process_one, entries):
            done += 1
            if ok:
                ok_count += 1
                mark = '✓'
            else:
                fail_count += 1
                mark = '↻'  # fallback used
            print(f'    [recrop {done:>2}/{total}] {mark} #{e["number"]:>2} '
                  f'{e["subject"]:>8} {reason or ""}', flush=True)
    return {'slug': slug, 'ok': ok_count, 'fallback': fail_count,
            'elapsed_s': int(time.time() - t0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rounds', nargs='*', help='Specific rounds; default: all under db/raw/')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--limit', type=int, default=0, help='Cap to first N rounds')
    args = ap.parse_args()

    if args.rounds:
        rounds = [r for r in args.rounds]
    else:
        rounds = [d.name for d in sorted((ROOT / 'db' / 'raw').iterdir())
                  if d.is_dir() and (d / '문제.pdf').exists()]
    if args.limit:
        rounds = rounds[:args.limit]
    print(f'recropping {len(rounds)} rounds (workers={args.workers})')

    summary = []
    for i, slug in enumerate(rounds, 1):
        print(f'\n══════ [{i}/{len(rounds)}] {slug} ══════', flush=True)
        try:
            r = recrop_round(slug, workers=args.workers)
        except Exception as e:
            r = {'slug': slug, 'error': str(e)[:200]}
        summary.append(r)
        if 'elapsed_s' in r:
            print(f'  ✓ {r["ok"]} cropped, {r["fallback"]} fallback ({r["elapsed_s"]}s)', flush=True)

    print('\n══════ Summary ══════')
    for r in summary:
        print(f'  {r}')


if __name__ == '__main__':
    main()
