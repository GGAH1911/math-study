#!/usr/bin/env python3
"""Fill `grade:` for every spoke by walking its prerequisites until we hit
a `concept_type: unit` (or another spoke with grade already set).

Spokes auto-created during ingest don't get a grade — the parent unit's
grade should propagate to them.

Idempotent: skips spokes that already have a `grade:` line.
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path('/home/insung/Projects/math-study/docs/concepts')


def parse_fm(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, full_text)."""
    text = path.read_text(encoding='utf-8')
    # Crude: scan for `key: value` lines until the second `---`
    fm: dict[str, str | list[str]] = {}
    if not text.startswith('---'):
        return fm, text
    end = text.find('---', 3)
    if end < 0:
        return fm, text
    block = text[3:end]
    for line in block.splitlines():
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('[') and val.endswith(']'):
            # crude list
            items = [s.strip().strip('"') for s in val[1:-1].split(',') if s.strip()]
            fm[key] = items
        else:
            fm[key] = val
    return fm, text


def slug_of(s: str) -> str:
    return s.split('/')[-1].replace('.md', '')


def main():
    all_files = sorted(CONCEPTS.glob('*.md'))
    print(f'concepts: {len(all_files)}', flush=True)

    # Pass 1: load every spoke's frontmatter
    fms: dict[str, dict] = {}
    texts: dict[str, str] = {}
    for p in all_files:
        fm, text = parse_fm(p)
        slug = p.stem
        fms[slug] = fm
        texts[slug] = text

    # Pass 2a: build reverse-prereq index so we can also propagate grades
    # in the opposite direction. If A's prereq is B, then B is presumably
    # the same grade as A.
    reverse: dict[str, list[str]] = {}
    for slug, fm in fms.items():
        for ref in (fm.get('prerequisites', []) if isinstance(fm.get('prerequisites'), list) else []):
            reverse.setdefault(slug_of(ref), []).append(slug)

    # Pass 2b: BFS resolve grade.
    # Try (a) own grade, (b) following prerequisites, (c) following the
    # reverse-prereq edge (some other spoke depending on me).
    cache: dict[str, str | None] = {}

    def resolve(slug: str, seen: set[str] | None = None) -> str | None:
        if slug in cache:
            return cache[slug]
        if seen is None: seen = set()
        if slug in seen:
            return None
        seen.add(slug)
        fm = fms.get(slug, {})
        my_grade = fm.get('grade') if isinstance(fm.get('grade'), str) else None
        if my_grade:
            cache[slug] = my_grade
            return my_grade
        # Forward: parent unit chain
        prereqs = fm.get('prerequisites', [])
        if not isinstance(prereqs, list):
            prereqs = []
        for ref in prereqs:
            pre_slug = slug_of(ref)
            g = resolve(pre_slug, seen)
            if g:
                cache[slug] = g
                return g
        # Reverse: any spoke that lists me as a prereq probably belongs
        # to the same grade.
        for child_slug in reverse.get(slug, []):
            g = resolve(child_slug, seen)
            if g:
                cache[slug] = g
                return g
        cache[slug] = None
        return None

    filled = 0
    skipped_already = 0
    no_chain = 0
    no_grade_examples: list[str] = []

    for p in all_files:
        slug = p.stem
        fm = fms[slug]
        existing = fm.get('grade')
        if isinstance(existing, str) and existing:
            skipped_already += 1
            continue
        target = resolve(slug)
        if not target:
            no_chain += 1
            if len(no_grade_examples) < 5: no_grade_examples.append(slug)
            continue
        text = texts[slug]
        # Insert/replace `grade:` line inside frontmatter.
        if re.search(r'^grade:\s*.*$', text, re.MULTILINE):
            new_text = re.sub(r'^grade:\s*.*$', f'grade: {target}', text,
                              count=1, flags=re.MULTILINE)
        else:
            # Insert right after `concept_type:` line if present, else after
            # the opening ---.
            if re.search(r'^concept_type:.*$', text, re.MULTILINE):
                new_text = re.sub(
                    r'^(concept_type:.*)$',
                    r'\1\n' + f'grade: {target}',
                    text, count=1, flags=re.MULTILINE)
            else:
                new_text = re.sub(r'^---\n', f'---\ngrade: {target}\n',
                                   text, count=1)
        p.write_text(new_text, encoding='utf-8')
        filled += 1

    print(f'\n═══ Summary ═══')
    print(f'  filled: {filled}')
    print(f'  already had grade: {skipped_already}')
    print(f'  no resolvable chain: {no_chain}')
    if no_grade_examples:
        print(f'  examples without chain: {", ".join(no_grade_examples)}')


if __name__ == '__main__':
    main()
