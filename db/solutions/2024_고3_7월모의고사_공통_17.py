import sympy as sp
x = sp.Symbol('x')
f = (x - 3) * (x**2 + x - 2)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 5)
if result == 50:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')