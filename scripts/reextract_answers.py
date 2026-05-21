#!/usr/bin/env python3
"""Re-extract answers for rounds whose problems.answer is NULL.

The text-layer parser (`_parse_answer_text` in ingest_round.py) was fixed
after the main batch ran: the header strip "N번 ~ M번" and the elective
markers for EBSi 통합본 PDFs now work. This script picks up any round that
still has NULL answers and re-runs the parser on its 정답.pdf, UPDATEing
DB rows + markdown frontmatter without touching crops or metadata.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import psycopg

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE / 'ingest_kice'))

from ingest_round import _extract_answers_from_text, DB, slugify_round  # noqa: E402

ROOT = _HERE.parent
DOCS_PROBLEMS = ROOT / 'docs' / 'problems'


def _rewrite_md_answer(slug: str, ans: str) -> bool:
    p = DOCS_PROBLEMS / f'{slug}.md'
    if not p.exists():
        return False
    text = p.read_text(encoding='utf-8')
    new_text, n = re.subn(
        r'^answer:\s*".*"$',
        f'answer: "{ans}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


def main():
    with psycopg.connect(DB) as conn:
        # Find exams that still have NULL answers
        rows = conn.execute("""
            SELECT e.id, e.year, e.exam_type, e.session, e.grade,
                   count(p.id) FILTER (WHERE p.answer IS NULL OR p.answer='') AS null_count,
                   count(p.id) AS total
            FROM exams e JOIN problems p ON p.exam_id = e.id
            GROUP BY e.id, e.year, e.exam_type, e.session, e.grade
            HAVING count(p.id) FILTER (WHERE p.answer IS NULL OR p.answer='') > 0
            ORDER BY e.year DESC, e.exam_type, e.grade, e.session
        """).fetchall()

    print(f'Rounds with NULL answers: {len(rows)}', flush=True)
    if not rows:
        return

    grand_updated = 0
    grand_remaining = 0
    skipped = []
    with psycopg.connect(DB, autocommit=True) as conn:
        for exam_id, year, exam_type, session, grade, null_count, total in rows:
            slug = slugify_round(year, exam_type, session, grade)
            ans_pdf = ROOT / 'db' / 'raw' / slug / '정답.pdf'
            if not ans_pdf.exists():
                print(f'  ⤳ {slug}: 정답.pdf 없음 — skip', flush=True)
                skipped.append(slug)
                grand_remaining += null_count
                continue
            try:
                # default subject for non-multisubject rounds
                if grade in ('고1', '고2'):
                    default_subject = '단일'
                elif exam_type == '검정고시':
                    default_subject = '단일'
                else:
                    default_subject = '공통'
                answers = _extract_answers_from_text(ans_pdf, default_subject, total)
            except Exception as e:
                print(f'  ✗ {slug}: parser error: {e}', flush=True)
                grand_remaining += null_count
                continue

            if not answers:
                print(f'  ⤳ {slug}: parser returned nothing — skip', flush=True)
                grand_remaining += null_count
                continue

            # Apply each (subject, number) → ans
            updated = 0
            for subj, m in answers.items():
                for num, ans in m.items():
                    n = int(num)
                    # Only update rows still NULL — don't overwrite trusted ones
                    r = conn.execute(
                        """UPDATE problems
                           SET answer=%s
                           WHERE exam_id=%s AND subject=%s AND number=%s
                             AND (answer IS NULL OR answer='')""",
                        (ans, exam_id, subj, n),
                    )
                    if r.rowcount:
                        updated += 1
                        _rewrite_md_answer(f'{slug}_{subj}_{n:02d}', ans)
            remaining = null_count - updated
            grand_updated += updated
            grand_remaining += remaining
            mark = '✓' if remaining == 0 else '⚠'
            print(f'  {mark} {slug}: +{updated}/{null_count} updated, {remaining} still NULL', flush=True)

    print(f'\n═══ Summary ═══')
    print(f'  filled: {grand_updated}')
    print(f'  still NULL: {grand_remaining}')
    print(f'  rounds without 정답.pdf: {len(skipped)}  ({", ".join(skipped[:10])}{"..." if len(skipped) > 10 else ""})')


if __name__ == '__main__':
    main()
