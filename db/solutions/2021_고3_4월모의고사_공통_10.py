import numpy as np
from sympy import symbols, integrate, solve, simplify

t, C = symbols('t C', real=True)
k = symbols('k', real=True, positive=True)

v = 4*t - 10
x = integrate(v, t) + C

x_at_1 = x.subs(t, 1)
x_at_k = x.subs(t, k)

eq = x_at_1 - x_at_k
sol = solve(eq, k)

k_val = [s for s in sol if s > 1]
if k_val and k_val[0] == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')