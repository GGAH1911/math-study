from sympy import *
x = symbols('x')
f_prime = x**3 + x
f = integrate(f_prime, x) - 1  # C = -1 from f(0) = -1
result = f.subs(x, 2)
print('VERIFY_PASS' if result == 5 else 'VERIFY_FAIL')