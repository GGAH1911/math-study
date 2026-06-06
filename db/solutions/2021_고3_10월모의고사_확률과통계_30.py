from fractions import Fraction
import math

# 확률 설정
p1, p2, p3, p4 = Fraction(1,3), Fraction(1,4), Fraction(1,4), Fraction(1,6)

# 조건 (가) 검증
P_X4 = p1**4
P_X16 = p4**4

assert P_X4 == Fraction(1, 81), f'P(X=4) = {P_X4}, expected 1/81'
assert P_X16 == Fraction(1, 1296), f'P(X=16) = {P_X16}, expected 1/1296'
assert P_X4 == 16 * P_X16, f'{P_X4} != 16*{P_X16}'

# 조건 (나) 검증
E_Y = 1*p1 + 2*p2 + 3*p3 + 4*p4
E_X = 4 * E_Y
assert E_X == 9, f'E(X) = {E_X}, expected 9'

# V(X) 계산
E_Y2 = 1*p1 + 4*p2 + 9*p3 + 16*p4
V_Y = E_Y2 - E_Y**2
V_X = 4 * V_Y

assert V_X == Fraction(19, 4), f'V(X) = {V_X}'

p, q = 4, 19
assert math.gcd(p, q) == 1, 'p and q must be coprime'
assert V_X == Fraction(q, p), f'V(X) = {V_X} != {q}/{p}'

print('VERIFY_PASS')