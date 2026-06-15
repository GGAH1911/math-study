import sympy as sp
x = sp.Symbol('x')
f = x/2 + sp.sin(x)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, sp.pi)
if result == sp.Rational(-1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')