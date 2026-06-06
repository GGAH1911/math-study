from sympy import *
x = symbols('x')
f_prime = x**3 + x
f = integrate(f_prime, x) + 3
assert f.subs(x, 0) == 3, 'Initial condition failed'
result = f.subs(x, 2)
assert result == 9, f'Expected 9, got {result}'
print('VERIFY_PASS')