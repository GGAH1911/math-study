#!/usr/bin/env python3
"""인제스트 일관성 게이트 — 조용한 데이터 결함 감지(마커 없는 손상).

A1. format 오분류: searchable_text에 보기마커(①②③④⑤)가 3개+ 있는데 format=numeric → choice 여야 함.
A2. numeric 비정수: format=numeric인데 answer가 정수(수능 단답 0-999)가 아님 → 손상/오분류 의심.
A3. answer_value 불일치: answer_value(값)와 answer(gold)가 둘 다 정수인데 다르면 의심.

→ A그룹(기하_23/24·단일_06: choice인데 numeric 오분류)·단일_18(보기 손상)류 재발 방지.
사용: python consistency_gate.py --all [--fix]   |   --list slug1,slug2 [--fix]
--fix: format 오분류만 자동교정(choice). 종료코드: 결함 있으면 1.
"""
from __future__ import annotations
import re, glob, sys, argparse
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
SEARCH = re.compile(r'^searchable_text:\s*[|>][-+]?\s*\n(.*?)(?=^\S|\Z)', re.M | re.S)
CHOICE_MARKS = re.compile(r'[①②③④⑤]')


def _extract(t):
    m = SEARCH.search(t)
    return m.group(1).strip() if m else ''


def check_one(md_path: str, fix: bool = False) -> list[str]:
    t = open(md_path, encoding='utf-8').read()
    txt = _extract(t)
    fmt = (re.search(r'(?m)^format:\s*(\w+)', t) or [None, 'numeric'])[1]
    ans = (re.search(r'''(?m)^answer:\s*['"]?([^'"\n]+)''', t) or [None, None])[1]
    ans = ans.strip().strip('\'"') if ans else None
    av = (re.search(r'''answer_value:\s*['"]?([^'"\n]+)''', t) or [None, None])[1]
    av = av.strip().strip('\'"') if av else None
    issues = []
    nmarks = len(set(CHOICE_MARKS.findall(txt)))
    if nmarks >= 3 and fmt == 'numeric':                          # A1
        issues.append('format-mismatch')
        if fix:
            t = re.sub(r'(?m)^format:\s*\w+', 'format: choice', t, count=1)
            open(md_path, 'w', encoding='utf-8').write(t)
    if fmt == 'numeric' and ans is not None and not re.fullmatch(r'-?\d+', ans):  # A2
        issues.append(f'numeric-noninteger({ans})')
    if fmt == 'numeric' and ans and av and re.fullmatch(r'-?\d+', ans) and re.fullmatch(r'-?\d+', av) \
            and ans != av:                                        # A3
        issues.append(f'ans≠value({ans}vs{av})')
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--fix', action='store_true')
    a = ap.parse_args()
    allmd = glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True)
    if a.all:
        paths = [p for p in allmd if 'README' not in p]
    elif a.list:
        idx = {Path(p).stem: p for p in allmd}
        paths = [idx[s.strip()] for s in a.list.split(',') if s.strip() in idx]
    else:
        print('--list 또는 --all 필요'); return
    flagged = []
    for p in paths:
        iss = check_one(p, a.fix)
        if iss:
            flagged.append((Path(p).stem, iss))
    c = Counter(i.split('(')[0] for _, iss in flagged for i in iss)
    print(f"검사 {len(paths)} · 결함 {len(flagged)}건  {dict(c)}", flush=True)
    for stem, iss in flagged[:40]:
        print(f"  - {stem}: {iss}", flush=True)
    sys.exit(1 if flagged else 0)


if __name__ == '__main__':
    main()
