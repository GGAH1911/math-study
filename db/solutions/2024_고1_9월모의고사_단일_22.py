from sympy import symbols, Poly
x, a = symbols('x a')
f = x**3 + 2*x**2 - 9*x + a
a_val = 13
f_val = f.subs([(x, 1), (a, a_val)])
if f_val == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')