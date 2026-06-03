import sympy as sp
from fractions import Fraction

# 구한 값들
P_A = Fraction(1, 2)
P_B = Fraction(2, 5)
P_A_and_B = Fraction(1, 5)
P_A_union_B = Fraction(7, 10)

# 조건 1: P(A|B) = P(A) = 1/2
P_A_given_B = P_A_and_B / P_B
assert P_A_given_B == P_A == Fraction(1, 2), f'조건 1 실패: P(A|B)={P_A_given_B}, P(A)={P_A}'

# 조건 2: P(A∩B) = 1/5
assert P_A_and_B == Fraction(1, 5), f'조건 2 실패: P(A∩B)={P_A_and_B}'

# 조건 3: 합사건 공식 검증
P_union_check = P_A + P_B - P_A_and_B
assert P_union_check == P_A_union_B, f'합사건 공식 실패: {P_union_check} != {P_A_union_B}'

print('VERIFY_PASS')