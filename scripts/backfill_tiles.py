#!/usr/bin/env python3
"""기존 코퍼스의 '세로 긴 문제'에 LLM 입력용 타일을 미리 생성(멱등).

튜터(chat.ts, Node)는 이미지 라이브러리가 없어 타일을 즉석 생성하지 못한다 →
타일이 디스크에 미리 있어야 한다. db/raw/<round>/images/*.png 를 훑어 다운스케일
대상(면적>1.15MP 또는 긴변>1568)만 tiles/ 하위폴더에 슬라이스한다. 짧은 문제는 건너뜀.

build_solution_cache(풀이 캐시)는 Python 이라 풀 때 알아서 생성하지만, 이미 캐시된
문제(재캐싱 안 함)는 타일이 없으므로 이 백필이 튜터용으로 미리 깔아둔다.
"""
from __future__ import annotations
import glob
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent           # = repo/worktree root
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiling import tile_for_vision, needs_tiling          # noqa: E402


def main() -> None:
    imgs = [
        f for f in glob.glob(str(ROOT / 'db' / 'raw' / '*' / 'images' / '*.png'))
        if '/tiles/' not in f
    ]
    tall = made = 0
    for f in sorted(imgs):
        p = Path(f)
        try:
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            continue
        if not needs_tiling(w, h):
            continue
        tall += 1
        tiles = tile_for_vision(p)
        if len(tiles) > 1:
            made += 1
            print(f'  {p.name}: {w}x{h} → {len(tiles)} 타일', flush=True)
    print(f'\n세로 긴 문제 {tall}장 · 타일셋 {made}개 생성/확인 완료', flush=True)


if __name__ == '__main__':
    main()
