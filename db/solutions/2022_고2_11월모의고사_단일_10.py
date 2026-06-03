import sympy as sp
x = sp.Symbol('x')
c = sp.Symbol('c')
f = x**2 - 6*x + c
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 4)
print('VERIFY_PASS' if result == 2 else 'VERIFY_FAIL')