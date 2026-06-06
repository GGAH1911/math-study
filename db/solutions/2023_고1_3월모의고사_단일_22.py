import sympy as sp
x, a = sp.symbols('x a')
eq = x**2 - 2*a*x + 5*a
a_val = 9
eq_sub = eq.subs(a, a_val)
result = eq_sub.subs(x, 3)
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')