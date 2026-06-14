import math
from sympy import *

# 원의 넓이로부터 반지름
R = 7*sqrt(3)/3
assert abs(pi*R**2 - Rational(49, 3)*pi) < 1e-10

# 사인 법칙: BC/sin(BAC) = 2R
BC = 2*R * sin(pi/3)
BC_val = simplify(BC)
assert BC_val == 7

# 코사인 법칙: BC² = AB² + AC² - 2·AB·AC·cos(∠BAC)
# 49 = 9 + AC² - 3AC
AC_sym = symbols('AC', positive=True, real=True)
eq = Eq(AC_sym**2 - 3*AC_sym - 40, 0)
AC_sol = solve(eq, AC_sym)
AC = [s for s in AC_sol if s > 0][0]
assert AC == 8

# 외심 O에서 AC까지의 거리
# 삼각형 OAC: OA = OC = R, AC = 8
# AC의 중점 M까지의 거리 AM = 4
# OM = sqrt(R² - 4²)
OM = sqrt(R**2 - 16)
OM_val = simplify(OM)
assert OM_val == sqrt(3)/3

# P에서 AC까지의 최대 거리
h_max = OM + R
h_max_val = simplify(h_max)
assert h_max_val == 8*sqrt(3)/3

# 삼각형 PAC의 최대 넓이
S_max = Rational(1, 2) * 8 * (8*sqrt(3)/3)
S_max_val = simplify(S_max)
assert S_max_val == 32*sqrt(3)/3

print('VERIFY_PASS')