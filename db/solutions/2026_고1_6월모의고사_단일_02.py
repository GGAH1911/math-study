import sympy as sp
x, a = sp.symbols('x a')
P = 2*x**3 - 5*x**2 + a*x - 3
P_at_1 = P.subs(x, 1)
a_value = sp.solve(P_at_1, a)[0]
if a_value == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')