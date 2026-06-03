import sympy as sp
x = sp.Symbol('x')
f = 4 * sp.ln(x)
f_double_prime = sp.diff(f, x, 2)
result = f_double_prime.subs(x, 2)
if result == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')