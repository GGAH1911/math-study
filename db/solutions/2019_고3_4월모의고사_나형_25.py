"""2019 고3 4월모의고사 나형 25번 — 파라미터 솔버 (수동 작성).
문제: 수열 {a_n}, Σ_{k=1}^{10} a_k = 30 일 때 Σ_{k=1}^{10}(k + a_k). (답 85)
구조: Σ(k+a_k) = Σk + Σa_k = 10·11/2 + 30 = 55 + 30 = 85.
재생산: (n, Σa_k) 파라미터화.
"""


def solve(n, sum_a):
    return n * (n + 1) // 2 + sum_a


CANDIDATE = 85
assert solve(10, 30) == CANDIDATE, solve(10, 30)
print('VERIFY_PASS')
