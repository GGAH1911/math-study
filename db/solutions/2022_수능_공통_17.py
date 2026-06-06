import sympy as sp
x = sp.Symbol('x')
f_prime = 3*x**2 + 2*x
f = sp.integrate(f_prime, x) + 2  # C = 2
result = f.subs(x, 1)
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')