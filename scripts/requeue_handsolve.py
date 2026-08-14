#!/usr/bin/env python3
"""`handsolve-pending` 인데 큐 파일이 없는 문제를 **큐에 되살린다.**

★왜 필요한가: 손풀이 큐(db/solutions/_handsolve/<slug>.json)는 "오케스트레이터가 직접 풀
  문제" 의 목록이다. 그런데 문제 md 의 `verifier: handsolve-pending` 과 큐 파일이 **따로**
  관리돼서, 큐 파일이 지워지면 그 문제는 **영원히 아무도 안 본다** —
  build_solution_cache 는 `solution:` 키만 보고 skip 하므로 다시 만들지도 않는다.
  (2026-08-14: 실패한 실행의 큐를 정리하다가 26건을 통째로 잃었다.)

md 를 진실로 보고 큐를 재구성한다. 멱등 — 이미 있는 큐는 건드리지 않는다.

사용: python3 scripts/requeue_handsolve.py [--round <라운드슬러그>] [--apply]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / 'docs' / 'problems'
QUEUE = ROOT / 'db' / 'solutions' / '_handsolve'
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'


def fm(text: str, key: str, default: str = '') -> str:
    m = re.search(rf'^\s*{key}:\s*"?([^"\n]+)"?\s*$', text, re.M)
    return m.group(1).strip() if m else default


def steps_of(text: str) -> list[str]:
    m = re.search(r'^\s*solution_steps:\s*\n((?:\s*-\s.*\n)+)', text, re.M)
    if not m:
        return []
    return [re.sub(r'^\s*-\s*', '', l).strip().strip('"\'') for l in m.group(1).splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', default='')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    QUEUE.mkdir(parents=True, exist_ok=True)

    made = skipped = 0
    for f in sorted(PROBLEMS.rglob('*.md')):
        if a.round and a.round not in str(f):
            continue
        t = f.read_text(encoding='utf-8')
        if fm(t, 'verifier') != 'handsolve-pending':
            continue
        if (QUEUE / f'{f.stem}.json').exists():
            skipped += 1
            continue
        # ★타일이 있으면 반드시 넣는다 — 도형 문제는 통이미지가 아니라 원해상도 타일을 봐야 한다.
        stem = f.stem
        tiles = sorted(str(p) for p in (ROOT / 'db' / 'raw').rglob(f'tiles/{stem}_t*.png'))
        entry = {
            'slug': stem,
            'round': f.parent.name if f.parent.parent.name.isdigit() else f.parent.name,
            'subject': fm(t, 'subject') or stem.split('_')[-2],
            'number': stem.split('_')[-1],
            'gold': fm(t, 'answer'),
            'format': fm(t, 'format'),
            'has_figure': fm(t, 'has_figure'),
            'tier': fm(t, 'killer_tier'),
            'reason': 'requeued:handsolve-pending (큐 파일 유실 복구)',
            'best_answer': fm(t, 'answer_value') or fm(t, 'answer'),
            'best_steps': str(steps_of(t)[:6]),
            'trace': '[]',
            'image': f'/problem-images/{stem}.png',
        }
        if tiles:
            entry['vision_tiles'] = tiles
            entry['instruction'] = '통이미지 대신 vision_tiles 를 Read 로 직접 보고 풀 것(도형 판독 필수).'
        print(f'  + {stem}  (gold={entry["gold"]}, tier={entry["tier"]}, 타일 {len(tiles)})')
        made += 1
        if a.apply:
            (QUEUE / f'{stem}.json').write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n{made}건 {"큐에 복구" if a.apply else "복구 대상 (--apply 로 실행)"} · 이미 있음 {skipped}건')
    return 0


if __name__ == '__main__':
    sys.exit(main())
