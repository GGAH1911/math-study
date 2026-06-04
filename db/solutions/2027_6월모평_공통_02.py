import sympy as sp
x = sp.Symbol('x')
f = 3*x**2 - x + 1
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')