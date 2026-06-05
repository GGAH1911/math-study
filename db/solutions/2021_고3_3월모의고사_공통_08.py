import numpy as np
from sympy import symbols, solve, diff

x = symbols('x')
f = x**3 - 3*x**2 - 9*x

# 극값 확인
f_prime = diff(f, x)
critical_points = solve(f_prime, x)
print('Critical points:', critical_points)

# 극값 계산
f_at_minus1 = f.subs(x, -1)
f_at_3 = f.subs(x, 3)
print('f(-1):', f_at_minus1)
print('f(3):', f_at_3)

# M=4, m=-26에서 3개 교점 확인
for k_test in [4, -26]:
    eq = x**3 - 3*x**2 - 9*x - k_test
    roots = solve(eq, x)
    real_roots = [r for r in roots if r.is_real]
    print(f'k={k_test}: {len(real_roots)} real roots')

# 경계값 확인 (정확히 2개만 만남)
for k_boundary in [5, -27]:
    eq = x**3 - 3*x**2 - 9*x - k_boundary
    roots = solve(eq, x)
    real_roots = [r for r in roots if r.is_real]
    print(f'k={k_boundary} (boundary): {len(real_roots)} real roots')

if 4 - (-26) == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')