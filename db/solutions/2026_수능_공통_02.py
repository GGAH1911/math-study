from sympy import *
x, h = symbols('x h')
f = 3*x**3 + 4*x + 1
f_prime = diff(f, x)
result = f_prime.subs(x, 1)
print('VERIFY_PASS' if result == 13 else 'VERIFY_FAIL')