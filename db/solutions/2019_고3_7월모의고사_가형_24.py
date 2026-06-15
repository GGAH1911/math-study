"""2019 고3 7월모의고사 가형 24번 — 파라미터 솔버 (수동).
X~B(72,p). E(2X-3)=45 → 2·np-3=45 → np=24 → p=1/3.
V(2X-3)=4·V(X)=4·np(1-p)=4·72·(1/3)(2/3)=64. (답 64)"""
from fractions import Fraction as F
def solve(n, a, b, E_lin):
    np_ = F(E_lin - b, a)                    # E(aX+b)=a·np+b → np=(E_lin-b)/a
    p = np_ / n
    return a**2 * n * p * (1 - p)            # V(aX+b)=a²·np(1-p)
assert solve(72, 2, -3, 45) == 64, solve(72,2,-3,45)
print('VERIFY_PASS')
