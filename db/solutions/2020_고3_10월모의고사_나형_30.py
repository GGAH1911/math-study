CANDIDATE = 80

from sympy import *

x = symbols('x')

# g(x) 정의
g_left  = -Rational(3,4)*x**4 + x**3          # x < 1
g_right = Rational(2,3)*x**3 - 4*x**2 + 6*x - Rational(29,12)  # x >= 1

# 연속성 확인
assert g_left.subs(x, 1) == g_right.subs(x, 1), 'continuity fail'

# g'(x)
gp_left  = diff(g_left, x)   # 3x^2(1-x)
gp_right = diff(g_right, x)  # 2(x-1)(x-3)

# 극대/극소 확인
local_max_val = g_right.subs(x, 1)
local_min_val = g_right.subs(x, 3)
assert local_max_val == Rational(1,4), 'local max fail'
assert local_min_val == -Rational(29,12), 'local min fail'

# S = |a1| + |a2|
a1 = -Rational(29,12)
a2 = Rational(1,4)
S = abs(a1) + abs(a2)
computed_30S = 30 * S

if computed_30S == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed 30S={computed_30S}, candidate={CANDIDATE}')
