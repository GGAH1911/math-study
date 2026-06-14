from sympy import *
from math import comb

CANDIDATE = 1

# 핵심 관계식: 조건을 만족하는 경우의 수 / 전체 경우의 수 = 3/14

# 조건을 만족하는 (a,b,c) 분포의 경우의 수
case_0_2_2 = comb(3, 0) * comb(4, 2) * comb(3, 2)  # 18
case_2_0_2 = comb(3, 2) * comb(4, 0) * comb(3, 2)  # 9
case_2_2_0 = comb(3, 2) * comb(4, 2) * comb(3, 0)  # 18

favorable = case_0_2_2 + case_2_0_2 + case_2_2_0

# 전체 4-부분집합의 개수
total = comb(10, 4)

# 확률 (기약분수)
prob = Rational(favorable, total)

# 검증: 확률이 3/14와 일치하는지
expected = Rational(3, 14)

if prob == expected:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")