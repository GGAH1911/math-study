#!/usr/bin/env python3
"""Fetch official KICE (한국교육과정평가원) 수학 문제지 + 정답표 PDFs.

Source: https://www.suneung.re.kr
  - boardID=1500229 → 수능 (11월 본수능)
  - boardID=1500236 → 모의평가 (6월/9월)

Usage:
  python fetch_kice_official.py [--years 2022 2023 2024 2025 2026]
"""
from __future__ import annotations
import argparse
import io
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
RAW = ROOT / 'db' / 'raw'

BASE = 'https://www.suneung.re.kr'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

BOARDS = [
    # (label, boardID, m_param, has_session_col)
    ('수능',     1500234, '0403',  False),   # 대학수학능력시험 (11월 본수능, year+subject)
    ('모의평가', 1500236, '030302', True),    # 모의평가 (year + session + subject)
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='replace')


def fetch_binary(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def list_math_posts(board_id: int, m_param: str, has_session_col: bool, max_pages: int = 20) -> list[dict]:
    """Return [{boardSeq, year, session, subject}] for 수학 posts in this board.
    Some boards have a 'session' column (모평: 6월/9월), others don't (수능)."""
    posts: list[dict] = []
    for page in range(1, max_pages + 1):
        url = f'{BASE}/boardCnts/list.do?type=default&page={page}&boardID={board_id}&m={m_param}&s=suneung'
        try:
            html = fetch(url)
        except Exception as e:
            print(f'  page {page} fetch error: {e}', file=sys.stderr)
            break
        if has_session_col:
            rows = re.findall(
                r'<tr[^>]*>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>',
                html,
            )
        else:
            rows = [
                (boardSeq, year, '11월 본수능', subject)
                for boardSeq, year, subject in re.findall(
                    r'<tr[^>]*>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]+class=.link.[^>]*>',
                    html,
                )
            ]
        if not rows:
            break
        for boardSeq, year, session, subject in rows:
            if '수학' not in subject:
                continue
            posts.append({
                'boardSeq': boardSeq,
                'year': int(year),
                'session': session.strip(),
                'subject': subject.strip(),
            })
    return posts


def extract_file_urls(boardSeq: str, board_id: int, m_param: str) -> dict[str, tuple[str, str]]:
    """Return {kind: (fileSeq, filename)} where kind ∈ {문제지, 정답표}."""
    url = f'{BASE}/boardCnts/view.do?boardID={board_id}&boardSeq={boardSeq}&lev=0&m={m_param}&s=suneung'
    html = fetch(url)
    out: dict[str, tuple[str, str]] = {}
    for seq, name in re.findall(r"fileDown\.do\?fileSeq=([a-f0-9]+)[^'\"<>]*['\"<>][^>]*>([^<]+)", html):
        nm = name.strip()
        if '문제' in nm and '문제지' not in out:
            out['문제지'] = (seq, nm)
        elif '정답' in nm and '정답표' not in out:
            out['정답표'] = (seq, nm)
    return out


def write_pdf_from_download(data: bytes, src_name: str, dst_path: Path) -> int:
    """Write PDF to dst. If the download is a ZIP (e.g. 홀수형+짝수형 PDFs bundled),
    extract the first PDF inside. Returns size written in bytes."""
    is_zip = src_name.lower().endswith('.zip') or data[:2] == b'PK'
    if not is_zip:
        dst_path.write_bytes(data)
        return len(data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        pdf_names = [n for n in z.namelist() if n.lower().endswith('.pdf')]
        if not pdf_names:
            raise RuntimeError(f'no PDF inside ZIP {src_name}')
        with z.open(pdf_names[0]) as src:
            pdf_bytes = src.read()
    dst_path.write_bytes(pdf_bytes)
    return len(pdf_bytes)


def slug_for(year: int, session: str) -> str:
    if '11월' in session or '수능' in session or session == '11':
        return f'{year}_수능'
    if '6월' in session: return f'{year}_6월모평'
    if '9월' in session: return f'{year}_9월모평'
    return f'{year}_{session.replace(" ", "_")}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--years', type=int, nargs='+', default=[2022, 2023, 2024, 2025, 2026])
    ap.add_argument('--dry-run', action='store_true', help='Just list, don\'t download')
    ap.add_argument('--force', action='store_true', help='Re-download even if files exist')
    args = ap.parse_args()

    target_years = set(args.years)
    all_targets = []
    for board_name, board_id, m_param, has_session_col in BOARDS:
        print(f'\n══ {board_name} (boardID={board_id}) ══')
        posts = list_math_posts(board_id, m_param, has_session_col)
        print(f'  {len(posts)} 수학 posts found')
        for p in posts:
            if p['year'] not in target_years:
                continue
            all_targets.append((board_id, m_param, p))

    print(f'\n══ Targets in years {sorted(target_years)}: {len(all_targets)} ══')
    for board_id, m_param, p in all_targets:
        slug = slug_for(p['year'], p['session'])
        round_dir = RAW / slug
        round_dir.mkdir(parents=True, exist_ok=True)
        prob_pdf = round_dir / '문제.pdf'
        ans_pdf = round_dir / '정답.pdf'

        need = (args.force
                or not prob_pdf.exists()
                or not ans_pdf.exists()
                or prob_pdf.stat().st_size < 50000)
        marker = ' (re-download)' if args.force else (' [already have]' if not need else '')
        print(f'\n  {slug}  boardSeq={p["boardSeq"]}{marker}')

        if not need or args.dry_run:
            continue

        try:
            file_seqs = extract_file_urls(p['boardSeq'], board_id, m_param)
        except Exception as e:
            print(f'    !! view.do error: {e}')
            continue

        for kind, dst_path in [('문제지', prob_pdf), ('정답표', ans_pdf)]:
            entry = file_seqs.get(kind)
            if not entry:
                print(f'    ✗ no {kind} file')
                continue
            fseq, src_name = entry
            url = f'{BASE}/boardCnts/fileDown.do?fileSeq={fseq}'
            try:
                data = fetch_binary(url)
                size = write_pdf_from_download(data, src_name, dst_path)
                tag = ' (extracted from ZIP)' if src_name.lower().endswith('.zip') else ''
                print(f'    ✓ {kind} → {dst_path.name} ({size//1024}KB){tag}')
            except Exception as e:
                print(f'    ✗ {kind} download failed: {e}')


if __name__ == '__main__':
    main()
