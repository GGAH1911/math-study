"""2019 고3 4월모의고사 가형 24번 — 파라미터 솔버.
문제: 계단형(직사각형이 어긋나게 쌓인) 도로망을 따라 A→P→B 로 가는 최단거리 경로의 수.

수학 구조:
  도로망은 세 층(row)의 정사각형 칸들이 계단 모양으로 이어져 만들어진 격자다.
    - 하단 행(y=0): x = 0 .. bottom_w-1 칸
    - 중간 행(y=1): x = 0 .. mid_w-1  칸
    - 상단 행(y=2): x = top_x0 .. top_x0+top_w-1 칸
  A=(0,0) 에서 출발해 지점 P=(Px,Py) 를 반드시 지나 B=(Bx,By) 로 가는, 오른쪽·위쪽
  으로만 움직이는(단조) 최단경로의 수를 구한다. 전체 경로 수는 (A→P 경로 수)×(P→B 경로 수)
  로 분해된다(P 를 반드시 지나야 하므로).

파라미터화 포인트:
  - bottom_w, mid_w, top_x0, top_w : 계단형 도로망 자체의 모양(각 행의 폭·시작점)을 결정.
  - Px, Py, Bx, By : 경유점 P 와 도착점 B 의 좌표. 이 값이 바뀌면 (A→P)×(P→B) 분해가
    통째로 달라지므로 답이 실제로 바뀐다(원문제: bottom_w=5, mid_w=6, top_x0=2, top_w=4,
    P=(4,2), B=(6,3) → 45).
  - 도로망 칸 목록(cells)에서 가로/세로 간선(H,V) 집합을 만들고, 그 간선만 따라가는
    단조경로 수를 DP(w(x,y)=w(x-1,y)+w(x,y-1), 간선이 있을 때만)로 정확히 센다
    (숫자를 직접 반환하지 않고 실제로 계산).
"""
from functools import lru_cache

PARAMS = dict(
    bottom_w=5,   # 하단 행 칸 수 (x = 0 .. bottom_w-1, y=0)
    mid_w=6,      # 중간 행 칸 수 (x = 0 .. mid_w-1, y=1)
    top_x0=2,     # 상단 행 시작 x
    top_w=4,      # 상단 행 칸 수 (x = top_x0 .. top_x0+top_w-1, y=2)
    Px=4, Py=2,   # 경유점 P 좌표
    Bx=6, By=3,   # 도착점 B 좌표
)


def _build_cells(prm):
    bw, mw, tx0, tw = prm['bottom_w'], prm['mid_w'], prm['top_x0'], prm['top_w']
    if bw <= 0 or mw <= 0 or tw <= 0:
        raise ValueError('행의 폭은 1 이상이어야 한다(빈 도로망은 문제가 성립하지 않음)')
    cells = [(x, 0) for x in range(bw)]
    cells += [(x, 1) for x in range(mw)]
    cells += [(x, 2) for x in range(tx0, tx0 + tw)]
    return cells


def _edges(cells):
    H, V = set(), set()
    for (cx, cy) in cells:
        H |= {(cx, cy), (cx, cy + 1)}          # 가로엣지 (x,y)-(x+1,y), 키=왼끝
        V |= {(cx, cy), (cx + 1, cy)}          # 세로엣지 (x,y)-(x,y+1), 키=아래끝
    return H, V


def _mono_paths(H, V, src, dst):
    """src→dst 로 가는, 존재하는 간선만 타고 오른쪽/위쪽으로만 움직이는 경로 수(DP)."""
    @lru_cache(None)
    def w(x, y):
        if (x, y) == src:
            return 1
        t = 0
        if (x - 1, y) in H:
            t += w(x - 1, y)   # 왼→오 간선 타고 도착
        if (x, y - 1) in V:
            t += w(x, y - 1)   # 아래→위 간선 타고 도착
        return t
    return w(*dst)


def solve(prm):
    cells = _build_cells(prm)
    H, V = _edges(cells)
    A = (0, 0)
    P = (prm['Px'], prm['Py'])
    B = (prm['Bx'], prm['By'])
    a_to_p = _mono_paths(H, V, A, P)
    p_to_b = _mono_paths(H, V, P, B)
    return a_to_p * p_to_b


def statement(prm):
    bw, mw, tx0, tw = prm['bottom_w'], prm['mid_w'], prm['top_x0'], prm['top_w']
    return (
        "그림과 같이 직사각형 모양으로 연결된 도로망이 있다. "
        f"하단 행은 x=0..{bw - 1}, 중간 행은 x=0..{mw - 1}, 상단 행은 x={tx0}..{tx0 + tw - 1} "
        "구간의 단위 칸들이 계단 모양으로 이어져 있다. "
        f"이 도로망을 따라 A={(0, 0)} 지점에서 출발하여 "
        f"P=({prm['Px']},{prm['Py']}) 지점을 지나 B=({prm['Bx']},{prm['By']}) 지점까지 "
        "최단거리로 가는 경우의 수를 구하시오."
    )


CANDIDATE = 45
assert solve(PARAMS) == CANDIDATE, solve(PARAMS)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
