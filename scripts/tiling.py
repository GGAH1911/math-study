#!/usr/bin/env python3
"""세로로 긴 문제 PNG를 LLM(vision) 입력용으로 타일링.

문제 이미지는 가로폭이 ~950으로 거의 고정이고 세로만 변수다. Claude vision 은
긴 변 1568px 또는 면적 ~1.15MP 를 넘으면 다운스케일하므로, 세로로 긴 문제는
글자가 뭉개진다. 다운스케일 대신 **가로 풀폭으로 위→아래 슬라이스**해 각 타일이
예산(1568·1.15MP) 안에 들게 하면 원해상도로 LLM 이 읽을 수 있다.

- 짧은 문제(예산 이내) → [원본] 1장 그대로.
- 긴 문제 → 같은 폴더의 tiles/ 하위폴더에 <stem>_t1.png, _t2.png, ... 로 캐시
  (있으면 재사용). 하위폴더라 UI·/progress 크롭 프리뷰(최상위만 읽음)엔 안 섞인다.
- 타일 경계는 OVERLAP 만큼 겹쳐, 수식·도형이 자르는 선에 걸려도 한쪽에서 온전히 보임.

build_solution_cache 와 ingest(신규 문제), 백필 스크립트가 공유한다. 튜터(chat.ts)는
생성된 타일 파일을 glob 으로 소비하므로 Node 측 이미지 라이브러리가 필요 없다.
"""
from __future__ import annotations
import math
from pathlib import Path

from PIL import Image

LONG_EDGE = 1568          # Claude vision 긴 변 한도
AREA_BUDGET = 1_150_000   # Claude vision 면적 한도 (~1.15MP, ≈1,600 토큰)
OVERLAP = 100             # 타일 경계 겹침(px)


def needs_tiling(w: int, h: int) -> bool:
    return (w * h) > AREA_BUDGET or max(w, h) > LONG_EDGE


def tile_for_vision(png_path) -> list[Path]:
    """png_path 를 타일링해 타일 경로 리스트 반환(짧으면 [png_path]).
    멱등: 타일이 이미 있으면 재생성하지 않는다."""
    png_path = Path(png_path)
    try:
        with Image.open(png_path) as im:
            w, h = im.size
            if not needs_tiling(w, h):
                return [png_path]
            # 타일 1장이 면적·긴변 예산 안에 들도록 최대 타일 높이 산정
            budget_h = max(1, min(LONG_EDGE, AREA_BUDGET // max(1, w)))
            usable = max(1, budget_h - 2 * OVERLAP)   # 겹침 제외 순수 진행분
            n = max(2, math.ceil(h / usable))
            base = math.ceil(h / n)
            tiles_dir = png_path.parent / 'tiles'
            tiles_dir.mkdir(exist_ok=True)
            tiles: list[Path] = []
            for i in range(n):
                out = tiles_dir / f'{png_path.stem}_t{i + 1}.png'
                if not out.exists():
                    top = max(0, i * base - OVERLAP)
                    bot = min(h, (i + 1) * base + OVERLAP)
                    im.crop((0, top, w, bot)).save(out)
                tiles.append(out)
            return tiles
    except Exception:
        # 디코드 실패 등 → 원본 한 장으로 폴백(없는 것보단 낫다)
        return [png_path]


def vision_paths(png_path) -> tuple[list[Path], bool]:
    """(타일 경로들, 타일링됨?) — 호출부 프롬프트 분기용 헬퍼."""
    tiles = tile_for_vision(png_path)
    return tiles, len(tiles) > 1


if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        ts = tile_for_vision(arg)
        for t in ts:
            with Image.open(t) as im:
                print(f'{t}  {im.size[0]}x{im.size[1]}  ({im.size[0]*im.size[1]/1e6:.2f}MP)')
