#!/usr/bin/env python3
"""타일링 한계 테스트.

세로 긴 killer(2028 예시 #27, 971x2180)를 N장으로 *강제* 분할했을 때 LLM(haiku,
튜터 모델)이 여전히 문제를 정확히 인식하는지 N을 키워가며 측정한다. 각 N마다
타일들을 Read 시키고 (1)함수·수열 (2)핵심 조건/비율 (3)구하는 것 을 요약하게 해,
ground truth(등차수열·log2x·1:4·삼각형 넓이 합 Σ)와 대조한다.

목적: '몇 장부터 인식 실패하는가 / 장수 무관하게 잘 되는가'를 경험적으로 확인.
"""
from __future__ import annotations
import math
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'db' / 'raw' / '2028_예시' / 'images' / '2028_예시_단일_27.png'
OVERLAP = 100
NS = [1, 2, 3, 5, 8, 12, 16, 20]


def slice_n(n: int, out_dir: Path):
    with Image.open(SRC) as im:
        w, h = im.size
        base = math.ceil(h / n)
        paths = []
        for i in range(n):
            top = max(0, i * base - OVERLAP)
            bot = min(h, (i + 1) * base + OVERLAP)
            out = out_dir / f'n{n:02d}_t{i + 1:02d}.png'
            im.crop((0, top, w, bot)).save(out)
            paths.append(out)
        return paths, (w, base + (OVERLAP if n > 1 else 0))


def ask(paths, out_dir: Path):
    listing = '\n'.join(f'{i + 1}. {p}' for i, p in enumerate(paths))
    prompt = (
        f"문제가 세로로 길어 위→아래 {len(paths)}장으로 나뉘었고 경계가 약간 겹칩니다:\n{listing}\n\n"
        f"위 {len(paths)}장을 **모두** Read 로 열어 하나의 문제로 이어 붙인 뒤, 이 문제의 "
        f"(1) 등장 함수·수열 (2) 핵심 조건/비율 (3) 구하는 것 을 3~4줄로 정확히 요약하라. 풀지는 말 것."
    )
    args = [
        'claude', '-p', '--model', 'haiku',
        '--allowedTools', 'Read', '--add-dir', str(out_dir),
        '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
        '--max-turns', str(len(paths) + 6), '--', prompt,
    ]
    t = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=360)
        out = (r.stdout or '').strip() or (r.stderr or '')[-400:]
        return out, time.time() - t
    except subprocess.TimeoutExpired:
        return '(TIMEOUT 360s)', time.time() - t


def main():
    with Image.open(SRC) as im:
        w, h = im.size
    print(f'원본 #27: {w}x{h} ({w * h / 1e6:.2f}MP)\nGround truth: 등차수열·y=log2(x)·OA비 1:4·삼각형 넓이 합 Σ(1..5)\n', flush=True)
    for n in NS:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            paths, (tw, th) = slice_n(n, td)
            print(f"\n{'=' * 64}\n[N={n:>2}] 타일 {tw}x{th} (~{tw * th / 1e6:.2f}MP/장)", flush=True)
            resp, dt = ask(paths, td)
            print(f"  ⏱ {dt:.0f}s\n  {resp}", flush=True)
    print('\n=== 완료 ===', flush=True)


if __name__ == '__main__':
    main()
