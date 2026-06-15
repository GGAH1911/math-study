from sympy import *
from sympy.abc import x, a
import numpy as np

CANDIDATE = 340

# 함수 정의 (a=6)
a_val = 6
f = x**2
g = x**3 - 2*a_val*x**2 + a_val**2*x

# 조건 검증
# (가) f(0) = g(0)
assert f.subs(x, 0) == g.subs(x, 0) == 0, "Condition (가) failed"

# (나-1) lim f(x)/x as x→0 = 0
limit_f = limit(f/x, x, 0)
assert limit_f == 0, f"Condition (나-1) failed: got {limit_f}"

# (나-2) lim g(x)/(x-a) as x→a = 0
limit_g = limit(g/(x-a_val), x, a_val)
assert limit_g == 0, f"Condition (나-2) failed: got {limit_g}"

# (다) integral condition
integral_diff = integrate(g - f, (x, 0, a_val))
assert integral_diff == 36, f"Condition (다) failed: got {integral_diff}"

# 답 검증: 3 * integral |f - g|
diff = f - g
abs_diff_integral = integrate(Abs(diff), (x, 0, a_val))
result = 3 * abs_diff_integral

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: Expected {CANDIDATE}, got {result}")