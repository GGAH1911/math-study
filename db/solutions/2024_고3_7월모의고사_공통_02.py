import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 + 5*x - 2
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')