#!/usr/bin/env python3
"""For every round in db/raw/*, vision-extract the 정답.pdf into JSON
and UPDATE problems.answer + frontmatter. Idempotent — re-uses cached
work/ans_p*.json if present. Runs answer-extraction calls in parallel
(ThreadPool 4 workers).
"""
from __future__ import annotations
import concurrent.futures as cf
import json
import re
import subprocess
import time
from pathlib import Path

import fitz
import psycopg

ROOT = Path('/home/insung/Projects/math-study')
RAW = ROOT / 'db' / 'raw'
PROBLEMS_DIR = ROOT / 'docs' / 'problems'
DB = 'postgresql://mathstudy:mathstudy@127.0.0.1:5434/mathstudy'

ANSWER_SYSTEM = """당신은 한국 수능 수학 정답표 이미지를 읽어 JSON으로 변환합니다.
형식: {"공통": {"번호": "정답"}, "확률과통계": {...}, "미적분": {...}, "기하": {...}}.
객관식은 1-5, 단답형은 수치. JSON만 출력. 코드펜스도 X."""


def slugify_round(round_dir: str) -> tuple[int, str, str]:
    """e.g. '2024_수능' -> (2024, '수능', '11월 본수능'); '2024_9월모평' -> (2024, '모의평가', '9월')"""
    m = re.match(r'(\d{4})_(.+)', round_dir)
    if not m:
        return None
    year = int(m.group(1))
    suffix = m.group(2)
    if suffix == '수능':
        return year, '수능', '11월 본수능'
    if '9월' in suffix:
        return year, '모의평가', '9월'
    if '6월' in suffix:
        return year, '모의평가', '6월'
    return year, suffix, suffix


def vision_extract_one_page(ans_png_path: Path, ans_pages_dir: Path) -> dict | None:
    cache = ans_png_path.parent.parent / f'work/{ans_png_path.stem}.json'
    if cache.exists() and cache.stat().st_size > 5:
        try:
            return json.loads(cache.read_text(encoding='utf-8'))
        except Exception:
            pass
    abs_png = str(ans_png_path.absolute())
    for attempt in range(3):
        try:
            r = subprocess.run(
                ['claude', '-p',
                 '--model', 'sonnet',
                 '--max-turns', '5',
                 '--output-format', 'text',
                 '--no-session-persistence',
                 '--add-dir', str(ans_pages_dir),
                 '--system-prompt', ANSWER_SYSTEM,
                 f'Read 툴로 {abs_png} 를 열고 정답표 JSON 출력.'],
                cwd=str(ans_pages_dir),
                capture_output=True, text=True, timeout=180,
            )
            out = r.stdout.strip()
            out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out, flags=re.MULTILINE)
            data = json.loads(out)
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            return data
        except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError):
            if attempt < 2:
                time.sleep(3)
    return None


def process_round(round_dir: Path) -> dict:
    name = round_dir.name
    parsed = slugify_round(name)
    if not parsed:
        return {'round': name, 'ok': False, 'reason': 'name parse'}
    year, exam_type, session = parsed
    ans_pdf = round_dir / '정답.pdf'
    if not ans_pdf.exists():
        return {'round': name, 'ok': False, 'reason': 'no 정답.pdf'}

    # Render answer pages if not already
    ans_pages_dir = round_dir / 'ans_pages'
    ans_pages_dir.mkdir(exist_ok=True)
    work_dir = round_dir / 'work'
    work_dir.mkdir(exist_ok=True)
    doc = fitz.open(ans_pdf)
    for i, page in enumerate(doc):
        p = ans_pages_dir / f'ans_p{i+1:02d}.png'
        if not p.exists():
            page.get_pixmap(dpi=200).save(p)
    doc.close()

    # Merge all pages
    combined: dict[str, dict[str, str]] = {}
    for png in sorted(ans_pages_dir.glob('ans_p*.png')):
        data = vision_extract_one_page(png, ans_pages_dir)
        if data:
            for subj, mapping in data.items():
                combined.setdefault(subj, {}).update({k: str(v) for k, v in mapping.items()})

    if not combined:
        return {'round': name, 'ok': False, 'reason': 'vision returned nothing'}

    # Update markdown + DB
    updated_md = 0
    updated_db = 0
    with psycopg.connect(DB) as conn, conn.cursor() as cur:
        for subj, mapping in combined.items():
            for num_str, ans in mapping.items():
                num = int(num_str)
                slug = f'{name}_{subj}_{num:02d}'
                md = PROBLEMS_DIR / f'{slug}.md'
                if md.exists():
                    text = md.read_text(encoding='utf-8')
                    new = re.sub(r'^answer:\s*"[^"]*"$', f'answer: "{ans}"', text, count=1, flags=re.MULTILINE)
                    if new != text:
                        md.write_text(new, encoding='utf-8')
                        updated_md += 1
                cur.execute(
                    """UPDATE problems SET answer = %s
                       WHERE subject = %s AND number = %s
                       AND exam_id IN (SELECT id FROM exams
                                       WHERE year=%s AND exam_type=%s AND COALESCE(session,'')=%s)""",
                    (ans, subj, num, year, exam_type, session),
                )
                if cur.rowcount > 0:
                    updated_db += 1
        conn.commit()
    return {'round': name, 'ok': True, 'md': updated_md, 'db': updated_db, 'subjects': list(combined.keys())}


def main():
    rounds = sorted(d for d in RAW.iterdir() if d.is_dir() and (d / '정답.pdf').exists())
    print(f'Rounds with 정답.pdf: {len(rounds)}', flush=True)

    # We process each round serially because each round has only 1-2 answer
    # pages — not worth parallelizing across rounds (would still be 1 page
    # per round at a time). The vision call is the bottleneck.
    summary = []
    for d in rounds:
        print(f'\n══════ {d.name} ══════', flush=True)
        r = process_round(d)
        summary.append(r)
        if r.get('ok'):
            print(f'  ✓ md={r["md"]}, db={r["db"]}, subjects={r["subjects"]}', flush=True)
        else:
            print(f'  ✗ {r.get("reason")}', flush=True)

    print('\n═══════ Summary ═══════')
    for s in summary:
        mark = '✓' if s.get('ok') else '✗'
        print(f'  {mark} {s["round"]:<20} {s}', flush=True)


if __name__ == '__main__':
    main()
