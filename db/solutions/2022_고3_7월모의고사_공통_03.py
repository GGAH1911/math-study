import sympy as sp
x = sp.Symbol('x')
f = x**3 + 2*x + 7
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')