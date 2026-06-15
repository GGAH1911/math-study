"""2019 고3 4월모의고사 가형 24번 — 파라미터 솔버 (수동 작성).
문제: 직사각형(계단형) 도로망. A→P→B 최단거리 경우의 수. (답 45)
그림 판독(단위셀, 좌하 좌표): 하단행 x=0..4(y=0), 중간행 x=0..5(y=1), 상단행 x=2..5(y=2).
      A=(0,0), P=(4,2), B=(6,3).
구조: 단조(우/상) 격자경로 DP. (A→P) × (P→B).
재생산: cells/지점 좌표 파라미터화 — 임의 비정형 격자에 일반.
"""
from functools import lru_cache

CELLS = [(x, 0) for x in range(5)] + [(x, 1) for x in range(6)] + [(x, 2) for x in range(2, 6)]


def edges(cells):
    H, V = set(), set()
    for (cx, cy) in cells:
        H |= {(cx, cy), (cx, cy + 1)}          # 가로엣지 (x,y)-(x+1,y), 키=왼끝
        V |= {(cx, cy), (cx + 1, cy)}          # 세로엣지 (x,y)-(x,y+1), 키=아래끝
    return H, V


def mono_paths(H, V, src, dst):
    @lru_cache(None)
    def w(x, y):
        if (x, y) == src:
            return 1
        t = 0
        if (x - 1, y) in H: t += w(x - 1, y)   # 왼→오
        if (x, y - 1) in V: t += w(x, y - 1)   # 아래→위
        return t
    return w(*dst)


def solve():
    H, V = edges(CELLS)
    A, P, B = (0, 0), (4, 2), (6, 3)
    return mono_paths(H, V, A, P) * mono_paths(H, V, P, B)


CANDIDATE = 45
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
