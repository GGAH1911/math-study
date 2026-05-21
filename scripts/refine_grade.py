#!/usr/bin/env python3
"""Re-assign each spoke's grade using a priority-based propagation.

Old propagate_grade.py picked the *first* unit reached via BFS. That's
wrong when the LLM mis-assigned prereqs — e.g. `곱의_미분_법칙` was
given `prerequisites: [삼각함수]` so it inherited grade=수학1 even
though it's clearly a 미적분 spoke.

New rule: walk *all* reachable units (both prereq + reverse), collect
their grades, and pick the most advanced one. Priority below mirrors
the Korean curriculum sequence:
  미적분 > 기하 / 확률과통계 > 수학2 > 수학1 > 고1 > 중3 > 중2 > 중1
"""
from __future__ import annotations
import re
from pathlib import Path

CONCEPTS = Path('/home/insung/Projects/math-study/docs/concepts')

PRIORITY = {
    '미적분':      9,
    '기하':        8,
    '확률과통계':  8,
    '수학2':       7,
    '수학1':       6,
    '고1':         5,
    '중3':         4,
    '중2':         3,
    '중1':         2,
    '미분류':      0,
}


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


def slug_of(s: str) -> str:
    return s.split('/')[-1].replace('.md', '')


def set_field(text: str, key: str, value: str) -> str:
    if re.search(rf'^{key}:\s*.*$', text, re.MULTILINE):
        return re.sub(rf'^{key}:\s*.*$', f'{key}: {value}', text, count=1, flags=re.MULTILINE)
    if re.search(r'^concept_type:.*$', text, re.MULTILINE):
        return re.sub(r'^(concept_type:.*)$', r'\1\n' + f'{key}: {value}',
                      text, count=1, flags=re.MULTILINE)
    return re.sub(r'^---\n', f'---\n{key}: {value}\n', text, count=1)


def main():
    all_files = sorted(CONCEPTS.glob('*.md'))
    fms = {}
    texts = {}
    for p in all_files:
        fm, text = parse_fm(p)
        fms[p.stem] = fm
        texts[p.stem] = text

    # Build forward (prereq) + reverse adjacency.
    forward: dict[str, list[str]] = {}
    reverse: dict[str, list[str]] = {}
    for slug, fm in fms.items():
        for ref in (fm.get('prerequisites', []) if isinstance(fm.get('prerequisites'), list) else []):
            r = slug_of(ref)
            forward.setdefault(slug, []).append(r)
            reverse.setdefault(r, []).append(slug)

    # Walk *only* the forward (prereq) graph. Including reverse causes
    # everything to leak into 미적분 because the most advanced units sit
    # at the top of the curriculum DAG and almost any spoke can reach
    # them via reverse edges.
    #
    # Among all units reachable forward, pick the highest-priority grade
    # — this gives us "the most specific course this spoke depends on"
    # rather than the random first hit BFS happened to encounter.
    def best_grade(start: str) -> str | None:
        seen = {start}
        queue = [start]
        candidates: set[str] = set()
        while queue:
            cur = queue.pop()
            fm = fms.get(cur, {})
            if fm.get('concept_type') == 'unit':
                g = fm.get('grade') if isinstance(fm.get('grade'), str) else None
                if g and g in PRIORITY:
                    candidates.add(g)
                # Don't keep walking past a unit — units are the leaves
                # in the curriculum tree direction we care about.
                continue
            for nxt in forward.get(cur, []):
                if nxt not in seen and nxt in fms:
                    seen.add(nxt)
                    queue.append(nxt)
        if not candidates:
            # Fall back to reverse for true orphans (no forward chain).
            seen2 = {start}; q2 = [start]; cand2: set[str] = set()
            while q2:
                cur = q2.pop()
                fm = fms.get(cur, {})
                if fm.get('concept_type') == 'unit':
                    g = fm.get('grade') if isinstance(fm.get('grade'), str) else None
                    if g and g in PRIORITY: cand2.add(g)
                    continue
                for nxt in reverse.get(cur, []):
                    if nxt not in seen2 and nxt in fms:
                        seen2.add(nxt); q2.append(nxt)
            if not cand2: return None
            return max(cand2, key=lambda g: PRIORITY[g])
        return max(candidates, key=lambda g: PRIORITY[g])

    changed = 0
    kept = 0
    new_dist: dict[str, int] = {}

    for p in all_files:
        slug = p.stem
        fm = fms[slug]
        # Don't touch unit nodes — their grade was hand-set.
        if fm.get('concept_type') == 'unit':
            g = fm.get('grade')
            if isinstance(g, str): new_dist[g] = new_dist.get(g, 0) + 1
            kept += 1
            continue
        g = best_grade(slug)
        if not g:
            kept += 1
            existing = fm.get('grade')
            if isinstance(existing, str): new_dist[existing] = new_dist.get(existing, 0) + 1
            continue
        prev = fm.get('grade') if isinstance(fm.get('grade'), str) else None
        new_dist[g] = new_dist.get(g, 0) + 1
        if prev == g:
            kept += 1
            continue
        text = texts[slug]
        p.write_text(set_field(text, 'grade', g), encoding='utf-8')
        changed += 1

    print(f'═══ Summary ═══')
    print(f'  changed: {changed}')
    print(f'  unchanged: {kept}')
    print(f'  new grade distribution:')
    for g in sorted(new_dist.keys(), key=lambda x: -PRIORITY.get(x, 0)):
        print(f'    {g}: {new_dist[g]}')


if __name__ == '__main__':
    main()
