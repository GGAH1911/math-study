"""2019 고3 3월모의고사 나형 28번 — 파라미터 솔버 (수동 작성).
문제: U={3의 배수 아닌 30 이하 자연수}. A⊂U, n(A)=4, 원소합=100.
      오름차순 x1<x2<x3<x4 일 때 x4-x3+x2-x1 의 최댓값. (답 10)
구조: U 에서 합 100 인 4원소 조합을 전수 탐색, (x4-x3+x2-x1) 최대.
재생산: (limit, 제외규칙, 크기 n, 목표합) 파라미터화.
"""
from itertools import combinations


def solve(limit=30, n=4, target=100):
    U = [x for x in range(1, limit + 1) if x % 3 != 0]
    best = None
    for combo in combinations(U, n):
        if sum(combo) == target:
            x = sorted(combo)
            val = x[3] - x[2] + x[1] - x[0]
            best = val if best is None else max(best, val)
    return best


CANDIDATE = 10
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
