import sympy as sp
from sympy import symbols, solve

x = symbols('x')
k_val = 4
eq = x**2 - k_val*x + 3
roots = solve(eq, x)

if sorted(roots) == [1, 3]:
    f_1 = eq.subs(x, 1)
    f_3 = eq.subs(x, 3)
    f_2 = eq.subs(x, 2)
    if f_1 == 0 and f_3 == 0 and f_2 < 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')