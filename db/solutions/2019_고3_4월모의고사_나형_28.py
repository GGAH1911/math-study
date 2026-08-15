"""2019 고3 4월모의고사 나형 28번 — 파라미터화 솔버.

문제: 한 변 1인 정사각형이 ncols×nrows 개 붙어 있는 격자 도로망. 왼쪽 아래 A=(0,0)
      에서 오른쪽 아래 B=(ncols,0) 로 이동하되, 같은 도로(간선)를 두 번 지나지 않는
      경로(trail) 중 '가로 방향으로 이동한 길이의 합'이 horiz_len, '전체 이동 길이'가
      total_len 인 경로의 개수를 구한다. (원문제: ncols=4, nrows=2, horiz_len=4,
      total_len=12 → 답 9)

수학 구조 파라미터화:
  - ncols, nrows : 격자의 가로·세로 칸 수 (도로망의 크기 = 정사각형 ncols*nrows 개)
  - total_len    : 전체 이동 간선 수 (경로 길이)
  - horiz_len    : 가로 방향으로 이동한 길이의 합
    (A→B 의 순변위는 ncols 이므로, 오른쪽 이동 횟수 R·왼쪽 이동 횟수 L 은
     R-L=ncols, R+L=horiz_len 을 만족해야 한다 — horiz_len 과 ncols 의 관계가
     '가로로만 우향 이동했는지, 왼쪽으로 되돌아간 구간이 있는지'를 가른다.)
  경로는 격자 위에서 간선을 중복 없이 사용하는 trail 을 DFS 로 전수 탐색하여 실제로
  '푼다' — 숫자를 박아 넣지 않고 구조(격자 크기·길이 조건)를 바꾸면 답도 달라진다.
"""


def count(ncols, nrows, total_len, horiz_len):
    if ncols <= 0 or nrows <= 0:
        raise ValueError('격자 크기는 1 이상이어야 한다')
    if total_len <= 0 or horiz_len < 0:
        raise ValueError('길이 조건이 올바르지 않다')

    A = (0, 0)
    B = (ncols, 0)
    adj = {}
    for i in range(ncols + 1):
        for j in range(nrows + 1):
            nb = []
            if i < ncols: nb.append((i + 1, j))
            if i > 0:     nb.append((i - 1, j))
            if j < nrows: nb.append((i, j + 1))
            if j > 0:     nb.append((i, j - 1))
            adj[(i, j)] = nb

    res = 0

    def dfs(cur, used, ne, nh):
        nonlocal res
        if ne == total_len:
            if cur == B and nh == horiz_len:
                res += 1
            return
        if nh > horiz_len:                       # 가로 이동 길이 초과 가지치기
            return
        if total_len - ne > len(adj) * 4:         # 남은 간선 수가 그래프 규모를 넘으면 가지치기
            return
        for nb in adj[cur]:
            e = frozenset((cur, nb))
            if e in used:
                continue
            used.add(e)
            dfs(nb, used, ne + 1, nh + (1 if nb[1] == cur[1] else 0))
            used.discard(e)

    dfs(A, set(), 0, 0)
    return res


PARAMS = dict(ncols=4, nrows=2, total_len=12, horiz_len=4)


def solve(prm):
    return count(prm['ncols'], prm['nrows'], prm['total_len'], prm['horiz_len'])


def statement(prm):
    ncols, nrows, total_len, horiz_len = prm['ncols'], prm['nrows'], prm['total_len'], prm['horiz_len']
    n_squares = ncols * nrows
    return (
        f"그림과 같이 한 변의 길이가 1인 정사각형 {n_squares}개로 이루어진 도로망이 있다. "
        f"이 도로망을 따라 A 지점(왼쪽 아래)에서 출발하여 B 지점(오른쪽 아래)에 도착할 때, "
        f"가로 방향으로 이동한 길이의 합이 {horiz_len}이고 전체 이동한 길이가 {total_len}인 "
        f"경우의 수를 구하시오. (단, 한 번 지나간 도로는 다시 지나지 않는다.)"
    )


CANDIDATE = 9

# 참고: 파라미터 결합 확인용 (개별 흔들기로 재현되는 값들)
#   nrows=3  → 54,  nrows=4  → 219,  horiz_len=6 → 78,  horiz_len=8 → 23
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
