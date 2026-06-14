import sympy as sp
from sympy import symbols, Abs, diff, solve
x = symbols('x', real=True)
a_val = 3
g = (x**2 - 9)*(x + a_val)
f_neg = -(x**2 - 9)*(x + 3)
f_prime = diff(f_neg, x)
crit = solve(f_prime, x)
f_at_1 = f_neg.subs(x, 1)
result = abs(f_at_1)
if result == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')