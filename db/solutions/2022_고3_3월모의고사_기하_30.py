import sympy as sp
from sympy import sqrt, symbols, solve

# 설정된 값
c_val = 8
a_val = 5
x_B = 6
y_B = sp.Rational(-24, 5)

# 포물선 P1: (x + c)^2 = -4a(y - a)
LHS1 = (x_B + c_val)**2
RHS1 = -4 * a_val * (y_B - a_val)
assert LHS1 == RHS1, f'P1 검증 실패: {LHS1} != {RHS1}'

# 포물선 P2: (x - c)^2 = 4a(y + a)
LHS2 = (x_B - c_val)**2
RHS2 = 4 * a_val * (y_B + a_val)
assert LHS2 == RHS2, f'P2 검증 실패: {LHS2} != {RHS2}'

# 조건 (가): A1C = 5√5
A1 = (-c_val, a_val)
C = (-c_val + 2*a_val, 0)
dist_A1C = sqrt((C[0] - A1[0])**2 + (C[1] - A1[1])**2)
assert dist_A1C == 5*sqrt(5), f'조건 (가) 실패: {dist_A1C} != 5√5'

# 조건 (나): |F1B| - |F2B| = 48/5
F1 = (-c_val, 0)
F2 = (c_val, 0)
dist_F1B = sqrt((x_B - F1[0])**2 + (y_B - F1[1])**2)
dist_F2B = sqrt((x_B - F2[0])**2 + (y_B - F2[1])**2)
diff = dist_F1B - dist_F2B
assert diff == sp.Rational(48, 5), f'조건 (나) 실패: {diff} != 48/5'

# 삼각형 넓이
area = sp.Rational(1, 2) * 16 * sp.Rational(24, 5)
result = 10 * area
assert result == 384, f'넓이 계산 실패: {result} != 384'

print('VERIFY_PASS')