import sympy as sp
x = sp.Symbol('x')
f = (2*x + 1)*(x**2 - 2*x + 5)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)
print('VERIFY_PASS' if result == 20 else 'VERIFY_FAIL')