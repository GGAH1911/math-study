import sympy as sp
x = sp.Symbol('x')
f_prime = (3*x - 4) / sp.sqrt(x - 1)
integral = sp.integrate(f_prime, (x, 2, 5))
result = float(integral)
if abs(result - 12.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')