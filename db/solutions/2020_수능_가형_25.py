from fractions import Fraction
from math import comb

# 2020 수능 가형 25: a=주사위5번 홀수횟수 ~ B(5,1/2), b=동전4번 앞면 ~ B(4,1/2).
# P(a-b=3) = q/p (서로소). p+q?
CANDIDATE = 137
P = Fraction(0)
for a in range(0, 6):
    for b in range(0, 5):
        if a - b == 3:
            P += Fraction(comb(5, a), 2**5) * Fraction(comb(4, b), 2**4)
q, p = P.numerator, P.denominator    # P = q/p = 9/128
print('VERIFY_PASS' if p + q == CANDIDATE else 'VERIFY_FAIL')
