import sympy as sp
import numpy as np
from sympy import sin, cos, pi, solve, simplify

x = sp.Symbol('x', real=True)

# 방정식 풀이
eq = sin(x)**2 - (cos(x)**2 + cos(x))
solutions_eq = solve(eq, x)

# 0 < x <= 2π 범위의 해
valid_solutions = []
for sol in solutions_eq:
    if sol.is_real:
        val = float(sol.evalf())
        if 0 < val <= 2*np.pi:
            valid_solutions.append(val)

# 부등식 sin(x) > cos(x) 검증
final_solutions = []
for val in valid_solutions:
    sin_val = float(sin(val).evalf())
    cos_val = float(cos(val).evalf())
    if sin_val > cos_val:
        final_solutions.append(val)

# 근과 검증
test_values = [np.pi/3, np.pi, 5*np.pi/3]
verified = []
for x_val in test_values:
    eq_check = abs(float((sin(x_val)**2 - (cos(x_val)**2 + cos(x_val))).evalf())) < 1e-10
    ineq_check = float(sin(x_val).evalf()) > float(cos(x_val).evalf())
    if eq_check and ineq_check:
        verified.append(x_val)

total = sum(verified)
expected = 4*np.pi/3
if abs(total - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')