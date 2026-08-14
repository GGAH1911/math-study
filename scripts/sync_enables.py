#!/usr/bin/env python3
"""Mirror every `prerequisites` reference into the target's `enables`.

Auto-generated spokes during ingest set their own `prerequisites: [unit]`
but never added themselves to the unit's `enables:` list. That leaves
~2.3k one-way links — fine for graph layout but bad for the wiki side
where a unit page should list everything that depends on it.

This script reads all concepts, builds the inverse map of prereq edges,
then rewrites each file's `enables:` line to include any missing entries.
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path(__import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))) / 'docs/concepts'  # ★레포 위치 자동(이동 내성)


def parse_fm(path: Path):
    text = path.read_text(encoding='utf-8')
    fm: dict = {}
    if not text.startswith('---'):
        return fm, text
    end = text.find('---', 3)
    if end < 0:
        return fm, text
    for line in text[3:end].splitlines():
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', line)
        if not m: continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith('[') and v.endswith(']'):
            fm[k] = [s.strip().strip('"') for s in v[1:-1].split(',') if s.strip()]
        else:
            fm[k] = v
    return fm, text


def slug_of(ref: str) -> str:
    return ref.split('/')[-1].replace('.md', '')


def set_list_line(text: str, key: str, items: list[str]) -> str:
    """Replace the `key: [...]` line with the new list."""
    serialized = '[' + ', '.join(items) + ']'
    if re.search(rf'^{key}:\s*\[.*\]\s*$', text, re.MULTILINE):
        return re.sub(rf'^{key}:\s*\[.*\]\s*$', f'{key}: {serialized}',
                      text, count=1, flags=re.MULTILINE)
    # Insert after prereq line if exists, else after concept_type.
    if re.search(rf'^{key}:\s*.*$', text, re.MULTILINE):
        return re.sub(rf'^{key}:\s*.*$', f'{key}: {serialized}',
                      text, count=1, flags=re.MULTILINE)
    if re.search(r'^prerequisites:.*$', text, re.MULTILINE):
        return re.sub(r'^(prerequisites:.*)$',
                      r'\1\n' + f'{key}: {serialized}',
                      text, count=1, flags=re.MULTILINE)
    return re.sub(r'^---\n', f'---\n{key}: {serialized}\n', text, count=1)


def main():
    all_files = sorted(CONCEPTS.glob('*.md'))
    fms: dict[str, dict] = {}
    texts: dict[str, str] = {}
    for p in all_files:
        fm, text = parse_fm(p)
        fms[p.stem] = fm
        texts[p.stem] = text

    # Build inverse: for each unit, which spokes list it as prereq?
    needs_enable: dict[str, set[str]] = {}
    for slug, fm in fms.items():
        for ref in (fm.get('prerequisites', []) or []):
            pre = slug_of(ref)
            if pre in fms:
                needs_enable.setdefault(pre, set()).add(slug)

    touched = 0
    added_total = 0
    samples: list[str] = []

    for slug, fm in fms.items():
        wanted = needs_enable.get(slug, set())
        if not wanted: continue
        existing_raw = fm.get('enables', []) or []
        existing = {slug_of(r) for r in existing_raw}
        missing = wanted - existing
        if not missing: continue

        # Preserve any non-conforming entries the file already had.
        # Build the new list = existing (canonicalized) + missing (sorted).
        canonical_existing = [slug_of(r) for r in existing_raw if slug_of(r) in fms]
        new_list_slugs = canonical_existing + sorted(missing)
        # Dedupe while preserving order
        seen = set(); deduped = []
        for s in new_list_slugs:
            if s in seen: continue
            seen.add(s); deduped.append(s)
        new_list_refs = [f'docs/concepts/{s}.md' for s in deduped]

        text = texts[slug]
        new_text = set_list_line(text, 'enables', new_list_refs)
        if new_text != text:
            Path(CONCEPTS / f'{slug}.md').write_text(new_text, encoding='utf-8')
            touched += 1
            added_total += len(missing)
            if len(samples) < 8:
                samples.append(f'{slug}: +{len(missing)} ({", ".join(list(missing)[:3])}{"..." if len(missing)>3 else ""})')

    print(f'═══ Summary ═══')
    print(f'  files modified: {touched}')
    print(f'  enables entries added (total): {added_total}')
    if samples:
        for s in samples: print(f'    {s}')


if __name__ == '__main__':
    main()
