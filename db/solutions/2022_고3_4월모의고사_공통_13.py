import sympy as sp
from sympy import symbols, integrate, limit, diff, simplify

x, t = symbols('x t', real=True)

# 조건을 만족하는 f(x) = 18x - 24 구성
f = 18*x - 24

# 검증 1: ∫_1^2 f(t)dt = 3
integral_f = integrate(f.subs(x, t), (t, 1, 2))
assert integral_f == 3, f"Expected 3, got {integral_f}"

# 검증 2: ∫_1^2 t*f(t)dt = 6
integral_tf = integrate(t * f.subs(x, t), (t, 1, 2))
assert integral_tf == 6, f"Expected 6, got {integral_tf}"

# 검증 3: 원래 극한 조건
integrand = (x - t) * f.subs(x, t)
integral_expr = integrate(integrand, (t, 1, x))
limit_val = limit(integral_expr / (x - 2), x, 2)
assert limit_val == 3, f"Expected 3, got {limit_val}"

# 검증 4: 구하는 값 계산
integral_result = integrate((4*x + 1) * f.subs(x, x), (x, 1, 2))
assert integral_result == 27, f"Expected 27, got {integral_result}"

print('VERIFY_PASS')