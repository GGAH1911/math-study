import sympy as sp
x = sp.Symbol('x')
f = (x + 1) * (x**2 + 3)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')