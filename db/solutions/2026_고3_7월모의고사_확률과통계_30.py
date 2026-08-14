# 주사위: 1→+1(1/6), 2→-1(1/6), 3이상→0(4/6). 7회 시행, a_n = n회 후 좌표.
# a_1=0, a_7=1 인 조건 아래 max{a_m} = 2 일 확률 q/p → p+q.
# 3^7 가지 걸음열을 전부 세어(가중치 정확 분수) 조건부확률을 실제로 계산한다.
CANDIDATE = 725
import sympy as sp
from itertools import product

W = {1: sp.Rational(1, 6), -1: sp.Rational(1, 6), 0: sp.Rational(4, 6)}
num = den = sp.Integer(0)
for steps in product((1, -1, 0), repeat=7):
    if steps[0] != 0:                       # a_1 = 0
        continue
    pos, mx, w = 0, 0, sp.Integer(1)
    for s in steps:
        pos += s; mx = max(mx, pos); w *= W[s]
    if pos != 1:                            # a_7 = 1
        continue
    den += w
    if mx == 2:
        num += w
prob = sp.nsimplify(num/den)
q, p = sp.fraction(prob)
print('VERIFY_PASS' if sp.Integer(p + q) == CANDIDATE and sp.gcd(p, q) == 1 else 'VERIFY_FAIL')
