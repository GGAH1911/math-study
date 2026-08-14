#!/usr/bin/env python3
"""Merge 4 duplicate placeholder unit nodes into their human-authored
equivalents. The placeholders were spawned during ingest when the LLM
chose a slightly different slug (e.g. `여러가지적분법` vs the existing
`여러가지_적분법`).

For each (from → to) pair:
  - rewrite every other concept's `prerequisites:` / `enables:` lines so
    references to the placeholder slug become references to the real unit
  - delete the placeholder .md file
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path(__import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))) / 'docs/concepts'  # ★레포 위치 자동(이동 내성)

MERGES = {
    '도함수의_활용':       '도함수의_활용_심화',
    '수열_극한':           '수열의_극한',
    '여러가지적분법':       '여러가지_적분법',
    '함수의_극한과_연속성': '함수의_극한과_연속',
}


def rewrite_refs(text: str) -> tuple[str, int]:
    """Replace placeholder slugs in `docs/concepts/<slug>.md` references."""
    n = 0
    for old, new in MERGES.items():
        old_ref = f'docs/concepts/{old}.md'
        new_ref = f'docs/concepts/{new}.md'
        if old_ref in text:
            text = text.replace(old_ref, new_ref)
            n += 1
    return text, n


def dedupe_list_line(line: str) -> str:
    """A list field may now contain duplicates (e.g. `[A, A]`) after the
    merge if both the placeholder and the real unit were referenced.
    Compact `[a, b, a]` → `[a, b]`."""
    m = re.match(r'^(\s*[a-zA-Z_]+:\s*)\[(.*)\]\s*$', line)
    if not m:
        return line
    prefix, body = m.group(1), m.group(2)
    items = [s.strip() for s in body.split(',') if s.strip()]
    seen = []
    for it in items:
        if it not in seen: seen.append(it)
    return f'{prefix}[{", ".join(seen)}]'


def main():
    files = list(CONCEPTS.glob('*.md'))
    print(f'scanning {len(files)} concept files', flush=True)
    touched = 0
    skipped_placeholders = []

    for p in files:
        slug = p.stem
        # Don't touch the placeholders themselves — they'll be deleted.
        if slug in MERGES:
            skipped_placeholders.append(p)
            continue
        text = p.read_text(encoding='utf-8')
        new_text, n = rewrite_refs(text)
        if n == 0:
            continue
        # Dedup list lines that may now contain repeats
        out_lines: list[str] = []
        for line in new_text.splitlines(keepends=False):
            stripped = line.lstrip()
            if stripped.startswith(('prerequisites:', 'enables:', 'concepts:')):
                out_lines.append(dedupe_list_line(line))
            else:
                out_lines.append(line)
        new_text = '\n'.join(out_lines) + ('\n' if new_text.endswith('\n') else '')
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            touched += 1

    # Delete placeholder files
    deleted = []
    for p in skipped_placeholders:
        try:
            p.unlink()
            deleted.append(p.stem)
        except Exception as e:
            print(f'  ! failed to delete {p.name}: {e}', flush=True)

    print(f'\n═══ Summary ═══')
    print(f'  spoke files rewritten: {touched}')
    print(f'  placeholders deleted:  {len(deleted)}  ({", ".join(deleted)})')


if __name__ == '__main__':
    main()
