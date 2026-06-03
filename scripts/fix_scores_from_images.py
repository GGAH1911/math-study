#!/usr/bin/env python3
"""Re-extract per-problem 배점 ([N점]) from problem-crop PNGs and correct
frontmatter `score` (+ body `# [...] N점` header) where it was wrong.

WHY: ingest's `ocr_client.convert_to_lwip_markdown` defaulted score to '3'
whenever full-page 2-column OCR missed the `[N점]` token (see ocr_client.py
`score = score_match.group(1) if score_match else '3'`). Per-problem crops
each contain exactly one [N점], so re-OCR'ing them recovers the true score.

Single OCR engines are noisy on the tiny [N점] token, so APPLY only fires when
tesseract AND DeepSeek-OCR AGREE on a value that differs from stored
(high precision — a lone engine's misread can't change a file). Everything
else is reported for human/vision review, never silently changed.

Usage:
  python scripts/fix_scores_from_images.py --dry-run            # tesseract, fast scale estimate → /tmp/score_audit.csv
  python scripts/fix_scores_from_images.py --apply             # ensemble (tess+deepseek agree) → write fixes
  python scripts/fix_scores_from_images.py --apply-list a,b,c   # apply an explicit slug=score list (vision-verified)
"""
from __future__ import annotations
import re, sys, glob, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VALID = {'2', '3', '4'}

# [N점] where N in 2..4. Bracket-anchored first (배점 is always bracketed) to
# avoid spurious '점' in problem bodies ("두 점", "100점" word problems, etc.).
_BR = re.compile(r'\[\s*([234])\s*점')
_LOOSE = re.compile(r'(?<![0-9])([234])\s*점\s*\]')


def _pick(text: str) -> str | None:
    br = _BR.findall(text)
    if br:
        return br[-1]            # 배점은 보통 stem 끝 = 마지막 bracket
    lo = _LOOSE.findall(text)
    return lo[-1] if lo else None


def tess_score(img: Path) -> str | None:
    try:
        out = subprocess.run(['tesseract', str(img), '-', '-l', 'kor+eng'],
                             capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return None
    return _pick(out)


def deepseek_score(img: Path) -> str | None:
    """Use the repo's DeepSeek-OCR client on the single-problem crop."""
    try:
        sys.path.insert(0, str(ROOT / 'scripts'))
        import ocr_client
        raw = ocr_client.ocr_page_raw(img, include_crops=False)
        if not raw:
            return None
        return _pick(raw.get('text', '') or '')
    except Exception:
        return None


def md_files() -> list[Path]:
    return [Path(f) for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)
            if 'README' not in f]


def stored_score(p: Path) -> str | None:
    t = p.read_text(encoding='utf-8')
    m = re.search(r'^\s*score:\s*(\d+)', t, re.M)
    return m.group(1) if m else None


def img_for(p: Path) -> Path:
    return IMGDIR / (p.stem + '.png')


def apply_fix(p: Path, new: str) -> bool:
    """Fix frontmatter `score:` and body `# [...] N점` header. Returns True if changed."""
    t = p.read_text(encoding='utf-8')
    t2 = re.sub(r'^(\s*score:\s*)\d+', rf'\g<1>{new}', t, count=1, flags=re.M)
    t2 = re.sub(r'^(#\s*\[[^\n\]]*\])\s*\d+\s*점', rf'\g<1> {new}점', t2, count=1, flags=re.M)
    if t2 != t:
        p.write_text(t2, encoding='utf-8')
        return True
    return False


def dry_run():
    rows = md_files()
    out = ROOT.parent / 'score_audit.csv' if False else Path('/tmp/score_audit.csv')
    resolved = unresolved = mismatch = 0
    default3_masked = misread = 0
    lines = ['slug,stored,tesseract,status']
    for p in rows:
        sc = stored_score(p)
        img = img_for(p)
        oc = tess_score(img) if img.exists() else None
        if oc is None:
            unresolved += 1
            lines.append(f'{p.stem},{sc},,unresolved')
            continue
        resolved += 1
        if oc != sc:
            mismatch += 1
            if sc == '3':
                default3_masked += 1   # 실제≠3 인데 default 3 으로 가려졌던 것
            else:
                misread += 1           # stored 가 비-3 (OCR 오인 or realign 오류)
            lines.append(f'{p.stem},{sc},{oc},MISMATCH')
        else:
            lines.append(f'{p.stem},{sc},{oc},ok')
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'total={len(rows)} resolved={resolved} unresolved={unresolved} '
          f'mismatch={mismatch} (default-3-masked={default3_masked}, stored-misread={misread})')
    print(f'audit → {out}')
    print('NOTE: tesseract-only. Real fixes need ensemble (--apply) — tesseract alone misreads ~some.')


def apply_ensemble():
    rows = md_files()
    fixed = conflict = unresolved = 0
    for p in rows:
        img = img_for(p)
        if not img.exists():
            continue
        sc = stored_score(p)
        t = tess_score(img)
        if t is None or t == sc:
            continue                      # tesseract agrees with stored or blank → leave
        d = deepseek_score(img)           # only spend a DeepSeek call when tesseract flags a change
        if d is None:
            unresolved += 1
            continue
        if d == t and d in VALID and d != sc:
            if apply_fix(p, d):
                fixed += 1
                print(f'  fix {p.stem}: {sc} → {d}')
        else:
            conflict += 1
            print(f'  CONFLICT {p.stem}: stored={sc} tess={t} deepseek={d} (skipped)')
    print(f'\napplied={fixed} conflicts={conflict} unresolved={unresolved}')


def apply_list(spec: str):
    """spec = 'slug=score,slug=score' — vision-verified manual overrides."""
    n = 0
    for item in spec.split(','):
        slug, _, val = item.partition('=')
        slug, val = slug.strip(), val.strip()
        if val not in VALID:
            print(f'  skip {slug}: bad score {val!r}'); continue
        matches = [Path(f) for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / f'{slug}.md'), recursive=True)]
        if not matches:
            print(f'  NOT FOUND {slug}'); continue
        if apply_fix(matches[0], val):
            n += 1; print(f'  fix {slug} → {val}')
        else:
            print(f'  no-change {slug} (already {val}?)')
    print(f'applied={n}')


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else '--dry-run'
    if arg == '--dry-run':
        dry_run()
    elif arg == '--apply':
        apply_ensemble()
    elif arg == '--apply-list' and len(sys.argv) > 2:
        apply_list(sys.argv[2])
    else:
        print(__doc__)
