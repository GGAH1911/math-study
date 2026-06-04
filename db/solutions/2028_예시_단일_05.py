import sympy as sp
x = sp.Symbol('x')
f = (x**2 - 1) * (2*x + 5)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, -1)
if result == -6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')