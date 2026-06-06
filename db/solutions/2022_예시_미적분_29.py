import sympy as sp
from sympy import exp, symbols, integrate, solve, simplify

# 함수 정의
x, u, t = symbols('x u t', real=True)
f = exp(x) + x - 1

# f(1), f(5) 계산
f_1 = f.subs(x, 1)
f_5 = f.subs(x, 5)

# 치환: t = f(u), dt = f'(u) du = (e^u + 1) du
# 적분: ∫ u/(1+e^u) * (e^u + 1) du = ∫ u du from u=1 to 5
integrand = u
result = integrate(integrand, (u, 1, 5))

if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')