#!/usr/bin/env python3
"""2D 격자 재조립 한계 테스트.

가로·세로 둘 다 큰(3000x2000=6MP) 합성 이미지에 distinct 3자리 숫자 6x6 격자를
그려 ground truth 를 확보한 뒤, 여러 타일링 방식으로 잘라 Haiku 가 전체를 이어붙여
6x6 숫자표를 정확히 전사하는지 자동 채점한다(/36).

비교 구성:
  - 1x1        : 전체 1장 → 다운스케일(블러) 베이스라인
  - 1D-6띠     : 가로 풀폭 6 가로띠 → 가로(3000)>1568 이라 각 띠도 다운스케일 (1D가 wide엔 무용)
  - 2x2/3x3/4x4: 2D 격자 (가로·세로 둘 다 분할 → 각 셀 원해상도)
"""
from __future__ import annotations
import math
import re
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = __import__('os').path.join(__import__('matplotlib').get_data_path(), 'fonts', 'ttf', 'DejaVuSans-Bold.ttf')  # ★matplotlib 이 자기 데이터 경로를 알려준다(옛 venv 하드코딩 제거)
W, H = 3000, 2000
ROWS, COLS = 6, 6
OVERLAP = 100
LONG_EDGE, AREA = 1568, 1_150_000

M = [
    [137, 482, 759, 263, 918, 504],
    [625, 391, 847, 172, 536, 980],
    [214, 768, 459, 803, 127, 695],
    [350, 641, 982, 415, 736, 208],
    [573, 829, 164, 947, 250, 681],
    [496, 312, 705, 538, 871, 124],
]
GT = [n for row in M for n in row]   # flatten 36


def make_image(path: Path):
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 96)
    cw, ch = W // COLS, H // ROWS
    for r in range(ROWS + 1):
        d.line([(0, r * ch), (W, r * ch)], fill=(180, 180, 180), width=3)
    for c in range(COLS + 1):
        d.line([(c * cw, 0), (c * cw, H)], fill=(180, 180, 180), width=3)
    for r in range(ROWS):
        for c in range(COLS):
            s = str(M[r][c])
            bb = d.textbbox((0, 0), s, font=f)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            d.text((c * cw + (cw - tw) / 2, r * ch + (ch - th) / 2 - bb[1]), s, fill='black', font=f)
    img.save(path)


def tile_grid(img: Image.Image, rows: int, cols: int, out_dir: Path):
    w, h = img.size
    cw, ch = math.ceil(w / cols), math.ceil(h / rows)
    tiles = []
    for r in range(rows):
        for c in range(cols):
            x0 = max(0, c * cw - (OVERLAP if cols > 1 else 0))
            x1 = min(w, (c + 1) * cw + (OVERLAP if cols > 1 else 0))
            y0 = max(0, r * ch - (OVERLAP if rows > 1 else 0))
            y1 = min(h, (r + 1) * ch + (OVERLAP if rows > 1 else 0))
            out = out_dir / f'r{r + 1}c{c + 1}.png'
            img.crop((x0, y0, x1, y1)).save(out)
            tiles.append((r + 1, c + 1, out, x1 - x0, y1 - y0))
    return tiles


def ask(tiles, rows, cols, out_dir: Path):
    listing = '\n'.join(f'  행{r}열{c}: {p}' for r, c, p, _, _ in tiles)
    if len(tiles) == 1:
        head = '아래 이미지는 6x6 숫자표 전체다.'
    else:
        head = (f'아래는 원본(6x6 숫자표)을 세로 {rows}행 × 가로 {cols}열 = {len(tiles)}조각으로 자른 것이다 '
                f'(행→열 순서, 경계가 약간 겹침). 모두 Read 로 열어 원본 한 장으로 이어 붙여라.')
    prompt = (
        f"{head}\n{listing}\n\n"
        f"원본에 있는 **6행 6열 숫자표**를 정확히 전사하라. 출력은 **오직 6줄**, 각 줄에 그 행의 6개 숫자만 "
        f"공백으로 구분해 적어라. 라벨·설명·다른 문자 절대 금지."
    )
    args = [
        'claude', '-p', '--model', 'haiku', '--allowedTools', 'Read', '--add-dir', str(out_dir),
        '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
        '--max-turns', str(len(tiles) + 6), '--', prompt,
    ]
    t = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=420)
        return (r.stdout or '').strip(), time.time() - t
    except subprocess.TimeoutExpired:
        return '(TIMEOUT)', time.time() - t


def score(resp: str):
    nums = [int(x) for x in re.findall(r'\d{1,4}', resp)][:36]
    correct = sum(1 for i, n in enumerate(nums) if i < len(GT) and n == GT[i])
    return correct, len(nums)


CONFIGS = [('1x1 전체(다운스케일)', 1, 1), ('1D 6가로띠', 6, 1),
           ('2x2', 2, 2), ('3x3', 3, 3), ('4x4', 4, 4)]


def main():
    with tempfile.TemporaryDirectory() as base:
        base = Path(base)
        src = base / 'grid.png'
        make_image(src)
        print(f'원본 {W}x{H} ({W * H / 1e6:.1f}MP) · 6x6 distinct 숫자 · GT 첫행 {M[0]}\n', flush=True)
        img = Image.open(src)
        for label, rows, cols in CONFIGS:
            td = base / label.replace(' ', '_').replace('(', '').replace(')', '')
            td.mkdir(exist_ok=True)
            tiles = tile_grid(img, rows, cols, td)
            tw, th = tiles[0][3], tiles[0][4]
            over = (tw * th > AREA) or (max(tw, th) > LONG_EDGE)
            print(f"\n{'=' * 60}\n[{label}] {len(tiles)}조각, 각 {tw}x{th} ({tw * th / 1e6:.2f}MP) "
                  f"{'→ 예산초과·다운스케일' if over else '→ 예산내·원해상도'}", flush=True)
            resp, dt = ask(tiles, rows, cols, td)
            ok, got = score(resp)
            print(f"  ⏱{dt:.0f}s · 정답 {ok}/36 (전사 {got}개)", flush=True)
            print('  ' + resp.replace('\n', '\n  '), flush=True)
    print('\n=== 완료 ===', flush=True)


if __name__ == '__main__':
    main()
