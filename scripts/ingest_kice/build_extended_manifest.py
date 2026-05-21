#!/usr/bin/env python3
"""Scrape horaeng.com category pages to discover round listing pages,
then for each round page extract the 수학 PDF URLs and build an
auto_complete_rounds manifest JSON.

Output: scripts/ingest_kice/rounds_extended.json
"""
from __future__ import annotations
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent / 'rounds_extended.json'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
TIMEOUT = 20

# Category pages on horaeng.com. Each is a listing of posts, one post per round.
# Pass raw Korean — fetch() URL-encodes once.
CATEGORIES: list[tuple[str, str]] = [
    ('고1-모의고사', 'category/고1 모의고사'),
    ('고2-모의고사', 'category/고2 모의고사'),
    ('고3-모의고사', 'category/고3 모의고사'),
    ('검정고시',    'category/검정고시'),
]

MIN_YEAR = 2022


def fetch(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    enc = urllib.parse.urlunsplit((parts.scheme, parts.netloc,
                                   urllib.parse.quote(parts.path, safe='/-._~'),
                                   parts.query, parts.fragment))
    req = urllib.request.Request(enc, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode('utf-8', errors='replace')


def head_ok(url: str) -> bool:
    parts = urllib.parse.urlsplit(url)
    enc = urllib.parse.urlunsplit((parts.scheme, parts.netloc,
                                   urllib.parse.quote(parts.path, safe='/-._~'),
                                   parts.query, parts.fragment))
    try:
        req = urllib.request.Request(enc, method='HEAD', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except Exception:
        return False


def crawl_category(cat_path: str, max_pages: int = 10) -> list[str]:
    """Return list of post URLs in this category, paginating until empty."""
    post_urls: set[str] = set()
    for page in range(1, max_pages + 1):
        url = f'https://horaeng.com/{cat_path}' + (f'/page/{page}' if page > 1 else '')
        try:
            html = fetch(url)
        except Exception as e:
            print(f'  ! page {page} fetch error: {e}', file=sys.stderr)
            break
        # horaeng post URLs are numeric, e.g. /257
        new = re.findall(r'href="(https://horaeng\.com/\d+)"', html)
        new_set = set(new) - post_urls
        if not new_set:
            break
        post_urls.update(new_set)
        print(f'  category page {page}: +{len(new_set)} posts (total {len(post_urls)})')
    return sorted(post_urls)


def parse_post_title(html: str) -> str:
    m = re.search(r'<title>([^<]+)</title>', html)
    return (m.group(1) if m else '').strip()


def extract_math_pdfs(html: str) -> dict[str, str]:
    """From a post page HTML, return {kind: url} where kind ∈ {문제,정답,해설}.
    Handles two naming styles:
      old: `...수학-문제.pdf` / `...수학-정답.pdf` / `...수학-해설.pdf`
      new: `...수학.pdf` (=문제) / `...수학-해설.pdf` / `...수학-해설-1.pdf`
    A 수학 PDF with NO 문제/정답/해설/풀이/답 marker after 수학 is treated as 문제."""
    urls = re.findall(r'href="(https?://horaeng\.com/wp-content/uploads/[^"]+\.pdf)"', html)
    urls = [u.replace('&amp;', '&') for u in urls if '수학' in urllib.parse.unquote(u)]
    out: dict[str, str] = {}
    for u in urls:
        dec = urllib.parse.unquote(u)
        # Take part after 수학
        idx = dec.rfind('수학')
        after = dec[idx+2:] if idx >= 0 else dec
        # 정답확정안 covers 검정고시 변형
        if '정답확정안' in after and '정답' not in out:
            out['정답'] = u
        elif '정답' in after and '정답' not in out:
            out['정답'] = u
        elif '해설' in after and '해설' not in out:
            out['해설'] = u
        elif '문제' in after and '문제' not in out:
            out['문제'] = u
        elif re.fullmatch(r'(?:-\d+)?\.pdf', after) and '문제' not in out:
            # e.g. 수학.pdf or 수학-1.pdf with no qualifier → treat as 문제
            out['문제'] = u
    return out


def parse_round_meta(category_label: str, title: str, post_url: str) -> dict | None:
    """From category + post title, infer (year, exam_type, session, grade).
    Returns None if year < MIN_YEAR or parse fails."""
    # year
    ym = re.search(r'(20\d{2})년', title) or re.search(r'(20\d{2})학년도', title)
    if not ym:
        return None
    year = int(ym.group(1))
    if year < MIN_YEAR:
        return None

    if category_label.startswith('고'):
        grade = category_label.split('-')[0]  # 고1/고2/고3
        # session = month
        mm = re.search(r'(\d{1,2})월', title)
        session = f'{mm.group(1)}월' if mm else '?'
        return {'year': year, 'exam_type': '모의고사', 'session': session, 'grade': grade,
                'agency': '교육청'}
    if category_label == '검정고시':
        # 중졸 / 고졸
        if '중졸' in title:
            grade = '중졸'
        elif '고졸' in title:
            grade = '고졸'
        else:
            return None
        # 회차 (제1회 / 제2회)
        rm = re.search(r'제\s*(\d)\s*회', title) or re.search(r'(\d)회', title)
        session = f'{rm.group(1)}회' if rm else '1회'
        return {'year': year, 'exam_type': '검정고시', 'session': session, 'grade': grade,
                'agency': '검정원'}
    return None


def main():
    entries: list[dict] = []
    unavailable: list[dict] = []

    for cat_label, cat_path in CATEGORIES:
        print(f'\n══ category {cat_label} ══')
        post_urls = crawl_category(cat_path)
        print(f'  → {len(post_urls)} posts')

        for purl in post_urls:
            try:
                html = fetch(purl)
            except Exception as e:
                print(f'    ! {purl}: fetch failed ({e})')
                continue
            title = parse_post_title(html)
            meta = parse_round_meta(cat_label, title, purl)
            if not meta:
                continue
            pdfs = extract_math_pdfs(html)
            problem = pdfs.get('문제')
            answer = pdfs.get('정답') or pdfs.get('해설')
            if not problem:
                unavailable.append({**meta, 'post': purl, 'reason': 'no 문제 PDF', 'title': title})
                continue
            entry = {**meta, 'pdf_url': problem, 'ans_url': answer, 'post': purl}
            entries.append(entry)
            print(f'    ✓ {meta["year"]} {meta.get("grade","")} {meta.get("session","")} ({meta["exam_type"]})')

    # Sort: year DESC, grade, session
    entries.sort(key=lambda e: (-(e['year']), e.get('grade') or '', e.get('session') or ''))

    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n══ Summary ══')
    print(f'  available: {len(entries)} rounds → {OUT}')
    print(f'  unavailable: {len(unavailable)} rounds')
    if unavailable:
        print('  unavailable details:')
        for u in unavailable[:10]:
            print(f'    - {u["year"]} {u.get("grade","")} {u.get("session","")} :: {u["reason"]} :: {u["title"][:60]}')

    # Per-type breakdown
    by_key: dict[tuple, int] = {}
    for e in entries:
        k = (e['exam_type'], e.get('grade'))
        by_key[k] = by_key.get(k, 0) + 1
    print('  by type:')
    for k, n in sorted(by_key.items()):
        print(f'    {k[0]} {k[1] or ""} : {n}')


if __name__ == '__main__':
    main()
