import sympy as sp
x = sp.Symbol('x')
f = (x + 1) * (x**2 + x - 5)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)
print('VERIFY_PASS' if result == 16 else 'VERIFY_FAIL')