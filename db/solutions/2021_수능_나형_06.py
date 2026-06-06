import sympy as sp
x = sp.Symbol('x')
f = x**4 + 3*x - 2
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)
if result == 35:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')