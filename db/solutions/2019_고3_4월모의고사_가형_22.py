"""2019 고3 4월모의고사 가형 22번 — 파라미터 솔버 (수동 작성).
문제: ₂Π₅ (중복순열) 의 값. (답 32)
구조: 중복순열 ₙΠ_r = n^r → ₂Π₅ = 2^5 = 32.
재생산: (n, r) 파라미터화.
"""


def nPi(n, r):
    return n ** r


CANDIDATE = 32
assert nPi(2, 5) == CANDIDATE, nPi(2, 5)
print('VERIFY_PASS')
