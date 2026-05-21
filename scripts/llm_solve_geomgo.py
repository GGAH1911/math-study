#!/usr/bin/env python3
"""Fill in missing answers for 검정고시 (중졸/고졸) rounds via Haiku.

The 검정고시 manifest entries have no ans_url, so 정답.pdf was never
downloaded and every problem ends up with answer=NULL. 검정고시 수학 is
중3/고1 level 4-choice — Haiku gets ~95% right.

Each problem is sent to Haiku twice; the answer is persisted only when
both passes agree (self-consistency). Mismatches are skipped + logged
so the user can sanity-check them later.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from pathlib import Path

import psycopg

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE / 'ingest_kice'))

from text_meta import _extract_problem_text  # noqa: E402
from ingest_round import claude_p, DB  # noqa: E402
from bbox import extract_problem_bboxes  # noqa: E402


ROOT = _HERE.parent
DOCS_PROBLEMS = ROOT / 'docs' / 'problems'

MODEL = 'haiku'
TIMEOUT_SEC = 30
CONSISTENCY_PASSES = 2
MIN_BODY_CHARS = 30

SOLVER_SYSTEM = """너는 한국 검정고시 수학 채점자다.
입력은 한 문제의 본문 텍스트 (PDF text-layer 추출, 일부 수식 글리프 ⋄ 누락 가능).
정답을 풀어 다음 JSON만 출력한다:

{ "answer": "N" }

규칙:
- 검정고시는 4지선다 — choice 면 N은 1~4 중 하나
- numeric (단답형) 이면 N은 정수
- 다른 텍스트/주석/코드펜스 금지. 풀이 과정 생략. 정답만.
"""

_JSON_RE = re.compile(r'\{[^{}]*"answer"[^{}]*\}', re.DOTALL)


def _parse_answer(out: str | None, fmt: str) -> str | None:
    if not out:
        return None
    out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
    m = _JSON_RE.search(out)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        ans = str(data.get('answer', '')).strip()
    except Exception:
        return None
    if not ans:
        return None
    if fmt == 'choice':
        return ans if ans in {'1', '2', '3', '4', '5'} else None
    if re.fullmatch(r'\d{1,3}', ans):
        return ans
    return None


def _solve_once(body: str, fmt: str, grade: str) -> str | None:
    user = f"학년: {grade}\nformat: {fmt}\n\n--- 본문 ---\n{body}\n\n위 문제의 정답을 JSON으로 답하라."
    out = claude_p(SOLVER_SYSTEM, user, model=MODEL, timeout=TIMEOUT_SEC, retries=1)
    return _parse_answer(out, fmt)


def _rewrite_md_answer(slug: str, ans: str, source: str = 'llm_haiku') -> bool:
    p = DOCS_PROBLEMS / f'{slug}.md'
    if not p.exists():
        return False
    text = p.read_text(encoding='utf-8')
    new_text, count = re.subn(
        r'^answer:\s*".*"$',
        f'answer: "{ans}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count == 0:
        return False
    if re.search(r'^answer_source:', new_text, re.MULTILINE):
        new_text = re.sub(r'^answer_source:.*$', f'answer_source: {source}',
                          new_text, count=1, flags=re.MULTILINE)
    else:
        new_text = re.sub(r'(^answer:\s*".*"$)',
                          r'\1\nanswer_source: ' + source,
                          new_text, count=1, flags=re.MULTILINE)
    p.write_text(new_text, encoding='utf-8')
    return True


def _slug_for_problem(frontmatter_path: str) -> str:
    return frontmatter_path.replace('docs/problems/', '').replace('.md', '')


def solve(slug_filter: list[str] | None = None) -> None:
    with psycopg.connect(DB) as conn:
        rows = conn.execute("""
            SELECT p.id, p.subject, p.number, p.format, p.frontmatter_path,
                   e.year, e.grade, e.session
            FROM problems p JOIN exams e ON e.id = p.exam_id
            WHERE e.exam_type = '검정고시'
              AND (p.answer IS NULL OR p.answer = '')
            ORDER BY e.year DESC, e.grade, e.session, p.number
        """).fetchall()

    if slug_filter:
        rows = [r for r in rows if any(s in r[4] for s in slug_filter)]

    print(f'== {len(rows)} problems to solve ==', flush=True)
    if not rows:
        return

    by_round: dict[str, dict] = {}
    # Pre-compute bbox entries per round so we don't re-parse the PDF per problem
    bbox_cache: dict[str, list[dict]] = {}

    for problem_id, subject, number, fmt, fm_path, year, grade, session in rows:
        round_slug = f'{year}_{grade}_{session}'
        st = by_round.setdefault(round_slug, {
            'tried': 0, 'confident': 0, 'inconsistent': 0, 'no_body': 0, 'errors': 0,
        })
        st['tried'] += 1

        if round_slug not in bbox_cache:
            pdf = ROOT / 'db' / 'raw' / round_slug / '문제.pdf'
            try:
                bbox_cache[round_slug] = extract_problem_bboxes(pdf, exam_type='검정고시', grade=grade)
            except Exception as e:
                print(f'  ✗ {round_slug} bbox extract failed: {e}', flush=True)
                bbox_cache[round_slug] = []
        entries = bbox_cache[round_slug]
        target = next((e for e in entries
                       if e['subject'] == subject and e['number'] == number), None)
        if not target:
            print(f'  ✗ {round_slug} #{number} {subject}: no bbox', flush=True)
            st['errors'] += 1
            continue

        pdf = ROOT / 'db' / 'raw' / round_slug / '문제.pdf'
        body = _extract_problem_text(pdf, target['page_num'], target['bbox_pdf'])
        if len(body.strip()) < MIN_BODY_CHARS:
            print(f'  ⤳ {round_slug} #{number} {subject}: body too short ({len(body)} chars)', flush=True)
            st['no_body'] += 1
            continue

        ans1 = _solve_once(body, fmt or 'choice', grade)
        ans2 = _solve_once(body, fmt or 'choice', grade)

        if ans1 and ans2 and ans1 == ans2:
            with psycopg.connect(DB, autocommit=True) as conn:
                conn.execute("UPDATE problems SET answer=%s WHERE id=%s", (ans1, problem_id))
            _rewrite_md_answer(_slug_for_problem(fm_path), ans1)
            st['confident'] += 1
            print(f'  ✓ {round_slug} #{number} {subject} fmt={fmt} → {ans1}', flush=True)
        else:
            st['inconsistent'] += 1
            print(f'  ⚠ {round_slug} #{number} {subject} inconsistent: {ans1!r} vs {ans2!r}', flush=True)

    print('\n═══ Summary ═══', flush=True)
    grand = {'tried': 0, 'confident': 0, 'inconsistent': 0, 'no_body': 0, 'errors': 0}
    for r, s in sorted(by_round.items()):
        rate = 100 * s['confident'] / max(s['tried'], 1)
        print(f'  {r}: {s["confident"]}/{s["tried"]} confident ({rate:.0f}%), '
              f'{s["inconsistent"]} inconsistent, {s["no_body"]} no-body, {s["errors"]} errors',
              flush=True)
        for k in grand: grand[k] += s.get(k, 0)
    print(f'\n  TOTAL: {grand["confident"]}/{grand["tried"]} '
          f'({100 * grand["confident"] / max(grand["tried"], 1):.0f}%)', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rounds', nargs='*', help='Specific round slugs to process')
    args = ap.parse_args()
    t0 = time.time()
    solve(slug_filter=args.rounds)
    print(f'\n  elapsed: {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
