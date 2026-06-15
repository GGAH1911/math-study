import sympy as sp
from sympy import symbols, solve, I, sqrt, simplify

CANDIDATE = 5

# 원래 삼차방정식
x = symbols('x')
eq = x**3 + x - 2

# 방정식의 모든 근
roots = solve(eq, x)
print(f"Three roots: {roots}")

# 실근과 허근 분리
real_roots = [r for r in roots if r.is_real]
complex_roots = [r for r in roots if not r.is_real]

print(f"Real root: {real_roots}")
print(f"Complex roots (alpha, beta): {complex_roots}")

alpha, beta = complex_roots[0], complex_roots[1]

# alpha^3 + beta^3 계산
alpha_cubed = simplify(alpha**3)
beta_cubed = simplify(beta**3)
result = simplify(alpha_cubed + beta_cubed)

print(f"alpha^3 = {alpha_cubed}")
print(f"beta^3 = {beta_cubed}")
print(f"alpha^3 + beta^3 = {result}")

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')