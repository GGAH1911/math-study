import sympy as sp
from sympy import symbols, I, expand, re, im

x = symbols('x')
# 원래 방정식
eq = x**3 + 2*x**2 - 3*x - 10

# 근들
roots = sp.solve(eq, x)
print(f'roots: {roots}')

# 허근 찾기
complex_roots = [r for r in roots if sp.im(r) != 0]
alpha, beta = complex_roots[0], complex_roots[1]
print(f'alpha={alpha}, beta={beta}')

# 검증: 원래 방정식 만족
verify_alpha = eq.subs(x, alpha)
verify_beta = eq.subs(x, beta)
print(f'eq(alpha)={sp.simplify(verify_alpha)}, eq(beta)={sp.simplify(verify_beta)}')

# alpha^3 + beta^3 계산
result = alpha**3 + beta**3
result_simplified = sp.simplify(result)
print(f'alpha^3+beta^3={result_simplified}')

if result_simplified == -4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')