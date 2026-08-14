#!/usr/bin/env python3
"""auto_complete_rounds — self-fixing orchestrator (manifest-driven).

Reads a manifest JSON of rounds, processes each via ingest_round.ingest_round(),
verifies actual problem count, self-fixes by clearing suspect page caches and
retrying up to MAX_SELF_FIX_PASSES. After all rounds, runs fill_spoke_bodies as
the closing stage.

Manifest entry shape:
  {
    "year": 2024, "exam_type": "모의고사", "session": "3월", "grade": "고3",
    "agency": "교육청", "pdf_url": "...", "ans_url": "...",
    "expected": 46     // optional override; default derived from EXPECTED_BY_TYPE
  }

Log format matches /api/progress parser (═════ headers + ✓/✗ + [N/M] spoke lines).
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))  # ★레포 위치 자동(이동 내성)
SCRIPTS = ROOT / 'scripts'
RAW = ROOT / 'db' / 'raw'
PROBLEMS_DIR = ROOT / 'docs' / 'problems'
FILL_SPOKE = SCRIPTS / 'fill_spoke_bodies.py'
INGEST_DIR = SCRIPTS / 'ingest_kice'
DEFAULT_MANIFEST = INGEST_DIR / 'rounds_manifest.json'
sys.path.insert(0, str(INGEST_DIR))

import ingest_round as ir  # noqa: E402  (kept for shared helpers)
import ingest_v2 as ir2     # noqa: E402  (PNG-First pipeline)

MAX_SELF_FIX_PASSES = 1  # v2 is more deterministic; one retry suffices

# Default expected problem count per exam_type. Per-round 'expected' in the
# manifest overrides this.
EXPECTED_BY_TYPE: dict[tuple[str, str | None], int] = {
    ('수능', None): 46,
    ('모의평가', None): 46,
    ('모의고사', '고3'): 46,
    ('모의고사', '고2'): 30,
    ('모의고사', '고1'): 30,
    ('학력평가', '고3'): 46,
    ('학력평가', '고2'): 30,
    ('학력평가', '고1'): 30,
    ('검정고시', '중졸'): 25,
    ('검정고시', '고졸'): 25,
}

# Built-in metadata for rounds we discovered before manifests existed.
# Used when --auto-detect picks up a raw/ directory not in any manifest.
LEGACY_ROUND_META: dict[str, dict] = {
    '2023_6월모평': dict(year=2023, exam_type='모의평가', session='6월'),
    '2023_9월모평': dict(year=2023, exam_type='모의평가', session='9월'),
    '2023_수능':    dict(year=2023, exam_type='수능',     session='11월 본수능'),
    '2024_6월모평': dict(year=2024, exam_type='모의평가', session='6월'),
    '2024_9월모평': dict(year=2024, exam_type='모의평가', session='9월'),
    '2024_수능':    dict(year=2024, exam_type='수능',     session='11월 본수능'),
    '2025_6월모평': dict(year=2025, exam_type='모의평가', session='6월'),
    '2025_9월모평': dict(year=2025, exam_type='모의평가', session='9월'),
    '2025_수능':    dict(year=2025, exam_type='수능',     session='11월 본수능'),
}


def expected_for(entry: dict) -> int:
    if entry.get('expected'):
        return int(entry['expected'])
    key = (entry['exam_type'], entry.get('grade'))
    if key in EXPECTED_BY_TYPE:
        return EXPECTED_BY_TYPE[key]
    # exam_type only (e.g. 수능/모의평가 ignore grade)
    return EXPECTED_BY_TYPE.get((entry['exam_type'], None), 46)


def slug_for(entry: dict) -> str:
    return ir.slugify_round(entry['year'], entry['exam_type'], entry.get('session'), entry.get('grade'))


def actual_count(round_slug: str) -> int:
    return len(list(PROBLEMS_DIR.glob(f'{round_slug}_*.md')))


def expected_numbers_per_page(pdf_path: Path) -> dict[int, set[int]]:
    """Use PyMuPDF text-layer to get canonical {page_num: {problem_numbers}}.
    Korean exam PDFs have problem numbers ("1.", "2.", "29.") as actual text
    even when formulas are in PUA glyphs."""
    out: dict[int, set[int]] = {}
    if not pdf_path.exists():
        return out
    try:
        d = fitz.open(pdf_path)
    except Exception:
        return out
    for i, p in enumerate(d):
        t = p.get_text()
        nums: set[int] = set()
        # "1.", "29." at line start (problem numbers)
        nums.update(int(n) for n in re.findall(r'(?:^|\n)\s*(\d{1,2})\.\s', t))
        # "1번" inline
        nums.update(int(n) for n in re.findall(r'(?:^|[\s\(])(\d{1,2})번', t))
        out[i + 1] = {n for n in nums if 1 <= n <= 50}
    d.close()
    return out


def detected_numbers_in_md(md_path: Path) -> set[int]:
    body = md_path.read_text(encoding='utf-8', errors='replace')
    return {int(m.group(1)) for m in re.finditer(r'^##\s*(\d+)\s*번', body, re.MULTILINE)}


def clear_suspect_pages(work_dir: Path, deficit: int = 0, pdf_path: Path | None = None) -> int:
    """Four-level suspect detection:
      1. MD caches that contain Korean Read-tool errors or no ## headers (bad).
      2. Pages where PNG exists but MD doesn't (vision timeout, no cache).
      3. If deficit > 0: clear pages whose ## detected numbers don't match the
         PDF text-layer ground truth (vision misread the problem number) — this
         catches the OCR-confusion case where vision saw "29" as "28" etc.
      4. Fallback: if PDF text isn't available, clear the LOWEST-## pages up to
         `deficit`, but only if their count is below median/2.
    Returns total count of work to retry on next ingest_round."""
    if not work_dir.exists():
        return 0
    removed = 0

    # Level 1: bad-cache MDs
    for md in work_dir.glob('p*.md'):
        try:
            body = md.read_text(encoding='utf-8')
        except Exception:
            continue
        head = body[:400]
        bad = ('## ' not in body) or ('찾을 수 없' in head) or ('권한' in head)
        if bad:
            md.unlink()
            removed += 1

    # Level 2: PNG without MD (timeout)
    pages_dir = work_dir.parent / 'pages'
    if pages_dir.exists():
        pngs = {int(p.stem[1:]) for p in pages_dir.glob('p*.png') if p.stem[1:].isdigit()}
        mds  = {int(p.stem[1:]) for p in work_dir.glob('p*.md')   if p.stem[1:].isdigit()}
        missing = pngs - mds
        if missing:
            print(f'    L2: {len(missing)} missing page MDs (vision timeout): {sorted(missing)[:10]}', flush=True)
        removed += len(missing)

    if deficit <= 0:
        return removed

    # Level 3: PDF text-layer cross-check (the strong signal)
    if pdf_path is None:
        pdf_path = work_dir.parent / '문제.pdf'
    expected_per_page = expected_numbers_per_page(pdf_path)
    mismatched: list[tuple[int, set[int], set[int]]] = []
    if expected_per_page:
        for md in work_dir.glob('p*.md'):
            page_num = int(md.stem[1:])
            expected = expected_per_page.get(page_num, set())
            if not expected:
                continue
            detected = detected_numbers_in_md(md)
            if detected != expected:
                mismatched.append((page_num, detected, expected))
        if mismatched:
            print(f'    L3: {len(mismatched)} pages mismatch PDF text-layer:', flush=True)
            for pn, det, exp in mismatched[:5]:
                missing_n = sorted(exp - det)
                extra_n = sorted(det - exp)
                print(f'      p{pn:02d} detected={sorted(det)} expected={sorted(exp)} missing={missing_n} extra={extra_n}', flush=True)
            for pn, _, _ in mismatched:
                p = work_dir / f'p{pn:02d}.md'
                if p.exists():
                    p.unlink()
                    removed += 1
            return removed

    # Level 4: fallback when PDF text isn't usable
    page_counts: list[tuple[Path, int]] = []
    for md in work_dir.glob('p*.md'):
        try:
            body = md.read_text(encoding='utf-8')
        except Exception:
            continue
        page_counts.append((md, body.count('## ')))
    if page_counts:
        counts = sorted(c for _, c in page_counts)
        median = counts[len(counts) // 2] if counts else 0
        threshold = max(1, median // 2)
        page_counts.sort(key=lambda kv: kv[1])
        cleared_for_deficit = 0
        for md, c in page_counts:
            if cleared_for_deficit >= deficit:
                break
            if c < threshold:
                md.unlink()
                cleared_for_deficit += 1
        if cleared_for_deficit:
            print(f'    L4: cleared {cleared_for_deficit} thin pages (count<{threshold}, median={median})', flush=True)
        removed += cleared_for_deficit
    return removed


def run_one(entry: dict) -> dict:
    slug = slug_for(entry)
    expected = expected_for(entry)
    label = f'{entry["exam_type"]}' + (f', {entry["grade"]}' if entry.get('grade') else '') + (f', {entry["session"]}' if entry.get('session') else '')
    print(f'\n══════ {slug} ══════', flush=True)
    print(f'  meta: {label}, expected={expected}', flush=True)

    final = {'round': slug, 'ok': False, 'count': 0, 'passes': 0}
    for attempt in range(1 + MAX_SELF_FIX_PASSES):
        plabel = 'initial' if attempt == 0 else f'self-fix #{attempt}'
        print(f'  [{plabel}] running ingest_round', flush=True)
        try:
            ir2.ingest_round_v2(
                year=entry['year'],
                exam_type=entry['exam_type'],
                session=entry.get('session'),
                pdf_url=entry.get('pdf_url'),
                ans_url=entry.get('ans_url'),
                grade=entry.get('grade'),
                agency=entry.get('agency', '평가원'),
            )
        except Exception as e:
            print(f'  [{plabel}] !! ingest_round_v2 error: {e}', flush=True)

        cnt = actual_count(slug)
        print(f'  [{plabel}] count={cnt}/{expected}', flush=True)
        partial = (RAW / slug / 'missing.json').exists()
        # Three-state outcome:
        #   ok=True, partial=False  → full success
        #   ok=True, partial=True   → ≥90% problems written + missing.json exists
        #   ok=False                → <90% or fatal error
        is_ok = (cnt >= expected) or (cnt >= expected * 0.9 and partial)
        final = {'round': slug, 'ok': is_ok, 'count': cnt,
                 'passes': attempt + 1, 'expected': expected, 'partial': partial}

        if cnt >= expected:
            print(f'  ✓ {slug} 완료 ({cnt}/{expected} 문제)', flush=True)
            return final

        work_dir = RAW / slug / 'work'
        deficit = max(0, expected - cnt)
        cleared = clear_suspect_pages(work_dir, deficit=deficit)
        print(f'  [{plabel}] cleared {cleared} suspect cache files', flush=True)
        if cleared == 0:
            # If we have a partial round (missing.json present and ≥90%),
            # accept it instead of looping — the Phase-2 LLM patcher will
            # fill the gaps. Re-running OCR/mapping on already-stuck pages
            # just costs Claude calls without recovering.
            if is_ok and partial:
                print(f'  ⚠ {slug} partial — no recoverable caches, accepting ({cnt}/{expected})', flush=True)
                return final
            print(f'  [{plabel}] no more suspect caches — giving up self-fix', flush=True)
            break

    if final.get('partial') and final.get('ok'):
        mark = '⚠'
        suffix = ' (partial)'
    elif final.get('ok'):
        mark = '✓'
        suffix = ''
    else:
        mark = '✗'
        suffix = ''
    print(f'  {mark} {slug} 최종 {final["count"]}/{final["expected"]} ({final["passes"]} passes){suffix}', flush=True)
    return final


def load_manifest(path: Path, augment_legacy: bool = False) -> list[dict]:
    """Load manifest exactly as-is. With augment_legacy=True, also include any
    legacy KICE rounds (수능/모평) on disk that aren't already in the manifest.
    Default off so explicit manifests aren't bloated with re-runs of done work."""
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    if augment_legacy:
        seen_slugs = {slug_for(e) for e in data}
        for slug, meta in LEGACY_ROUND_META.items():
            if slug in seen_slugs:
                continue
            if (RAW / slug / '문제.pdf').exists():
                data.append({**meta, 'agency': '평가원'})
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', default=str(DEFAULT_MANIFEST))
    ap.add_argument('--skip-spoke-fill', action='store_true', help='Skip final fill_spoke_bodies step')
    ap.add_argument('--augment-legacy', action='store_true', help='Also include legacy KICE rounds on disk')
    args = ap.parse_args()

    print(f'=== auto_complete_rounds START {datetime.now().isoformat(timespec="seconds")} ===', flush=True)
    print(f'Manifest: {args.manifest}{" (+legacy)" if args.augment_legacy else ""}', flush=True)
    entries = load_manifest(Path(args.manifest), augment_legacy=args.augment_legacy)
    print(f'Rounds to process: {len(entries)}', flush=True)

    summary = []
    for entry in entries:
        try:
            summary.append(run_one(entry))
        except Exception as e:
            slug = slug_for(entry)
            print(f'  ✗ {slug} CRASH: {e}', flush=True)
            summary.append({'round': slug, 'ok': False, 'count': 0, 'reason': str(e)})

    print('\n══════ Summary ══════', flush=True)
    n_ok = n_partial = n_fail = 0
    for s in summary:
        if s.get('partial') and s.get('ok'):
            mark = '⚠'; n_partial += 1; tag = ' partial'
        elif s.get('ok'):
            mark = '✓'; n_ok += 1; tag = ''
        else:
            mark = '✗'; n_fail += 1; tag = ''
        print(f'  {mark} {s["round"]:<30} count={s.get("count","?")}/{s.get("expected","?")} passes={s.get("passes","?")}{tag}', flush=True)
    print(f'\n  TOTAL: ✓ {n_ok}  ⚠ {n_partial} (partial — see db/raw/*/missing.json)  ✗ {n_fail}', flush=True)

    if not args.skip_spoke_fill:
        print(f'\n=== [final] fill_spoke_bodies {datetime.now().isoformat(timespec="seconds")} ===', flush=True)
        rc = subprocess.call([str(ROOT / '.venv' / 'bin' / 'python'), '-u', str(FILL_SPOKE)])
        print(f'=== [final] fill_spoke_bodies exit={rc} ===', flush=True)

    print(f'\n=== DONE {datetime.now().isoformat(timespec="seconds")} ===', flush=True)


if __name__ == '__main__':
    main()
