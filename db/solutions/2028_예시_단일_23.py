import sympy as sp
x = sp.Symbol('x')
f = x**3 - 4*x + 5
f_prime = sp.diff(f, x)
print('VERIFY_PASS' if f_prime == 3*x**2 - 4 and f.subs(x, 2) == 5 and f.subs(x, 4) == 53 else 'VERIFY_FAIL')