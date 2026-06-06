import sympy as sp
x = sp.Symbol('x')
f = (x**2 + 3*x) * (x**2 - x + 2)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)
if result == 58:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')