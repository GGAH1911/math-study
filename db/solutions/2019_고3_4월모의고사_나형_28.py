"""2019 고3 4월모의고사 나형 28번 — 파라미터 솔버 (수동 작성).
문제: 한 변 1인 정사각형 8개(4×2 격자) 도로망. A(좌하)→B(우하), 가로 이동 길이 합 4,
      전체 이동 길이 12, 한 번 지난 도로 재통과 금지. 경우의 수. (답 9)
구조: 4×2 격자 노드 (i,j) i=0..4,j=0..2. A=(0,0),B=(4,0). 가로 4 = 순변위 4 ⇒ 가로는 모두 우향.
      세로 8(=12-4). 중복 없는 trail(간선 비반복) 중 끝점 B·간선 12·가로 4 인 것 DFS 카운트.
재생산: 격자 폭(ncols)·길이/가로 제약 파라미터화.
"""


def count(ncols=4, nrows=2, total_len=12, horiz_len=4):
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
        if nh > horiz_len:                       # 가로 초과 가지치기
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


CANDIDATE = 9
assert count() == CANDIDATE, count()
print('VERIFY_PASS')
