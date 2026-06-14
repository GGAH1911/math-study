from sympy import symbols, diff, limit
x, h, a = symbols('x h a')
f = x**3 - 2*x**2 + a*x + 1
deriv_at_2 = f.diff(x).subs(x, 2)
from sympy import solve
a_val = solve(deriv_at_2 - 9, a)[0]
print('VERIFY_PASS' if a_val == 5 else 'VERIFY_FAIL')