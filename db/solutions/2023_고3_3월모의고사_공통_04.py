import sympy as sp
from sympy import symbols, integrate, diff

x, a_var = symbols('x a')
f = 3*x**2 - 2

# 원래 조건: ∫_1^x f(t) dt = x^3 - ax + 1
lhs = integrate(f, (x, 1, x))
rhs = x**3 - 2*x + 1

# a=2일 때 조건 확인
if sp.simplify(lhs - rhs) == 0:
    f_at_2 = f.subs(x, 2)
    if f_at_2 == 10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')