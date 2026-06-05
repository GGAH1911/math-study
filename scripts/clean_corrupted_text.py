#!/usr/bin/env python3
"""치환문자(⋄ � □ ◇)로 깨진 searchable_text를 regenerate로 청소 (텍스트 품질).
대상 = searchable_text에 깨짐 문자가 있는 문제만 (결정론적 선정, $0).
게이트(비회귀): 새 전사가 **깨짐 없고** 충분 길이면 채택(⋄-garbage보다 strictly 나음).
              전사 실패 or 여전히 깨짐이면 revert(원본 불변).
보너스: escalated(solved_by≠haiku)인데 새 텍스트로 풀리면(pass@K) → relabel(haiku+text_ok).
멱등: 현재 텍스트에 깨짐 없으면 skip. 환경: CC_K(3), CC_WORKERS(8)."""
from __future__ import annotations
import re, glob, os, sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import recover_text_defects as R   # noqa: E402  (transcribe, solve_passk, overwrite_text, relabel_md 재사용)
import build_solution_cache as B   # noqa: E402

CORRUPT = re.compile(r'[⋄�□◇]')
K = int(os.environ.get('CC_K', '3'))
WORKERS = int(os.environ.get('CC_WORKERS', '8'))
R.K = K   # solve_passk가 쓰는 K 동기화


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(ans=g('answer'), fmt=g('format'), sb=g('solved_by'))


def targets():
    out = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        if CORRUPT.search(B.extract_searchable(t)):   # 깨짐 있는 것만
            out.append((Path(f), meta(t)))
    return out


def clean(item):
    p, m = item
    new = R.transcribe(p.stem)
    if not new or CORRUPT.search(new):                # 전사 실패 or 여전히 깨짐 → revert(불변)
        return 'regen-fail'
    R.overwrite_text(p, new)                           # 깨끗한 전사 채택 (품질↑)
    if m['sb'] in ('sonnet', 'opus') and m['ans'] and R.solve_passk(new, m['fmt'], m['ans']):
        R.relabel_md(p)                                # 보너스: 난이도 정화 + 튜터 게이트
        return 'clean+relabel'
    return 'clean'


def main():
    tg = targets()
    print(f"═══ 깨짐 텍스트(⋄ � □ ◇) 청소 — {len(tg)}개 ═══", flush=True)
    print("  새 전사가 깨짐 없으면 채택(품질↑) · escalated+풀리면 relabel(보너스) · 실패=revert(불변)\n", flush=True)
    res = []
    TAG = {'clean': '✅ 청소', 'clean+relabel': '✅ 청소+relabel(난이도정화)', 'regen-fail': '⚠ regen-fail(revert·불변)'}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(clean, it): it for it in tg}
        for fut in as_completed(futs):
            it = futs[fut]; r = fut.result(); res.append(r)
            print(f"  [{len(res)}/{len(tg)}] {it[0].stem:34s} {TAG[r]}", flush=True)
    by = Counter(res)
    cleaned = by['clean'] + by['clean+relabel']
    print(f"\n═══ 완료 ═══ {dict(by)}", flush=True)
    print(f"  텍스트 청소 {cleaned}/{len(res)} (검색·튜터·솔버 품질↑) · 그중 relabel {by['clean+relabel']} · 실패 {by['regen-fail']}(원본 보존)", flush=True)


if __name__ == '__main__':
    main()
