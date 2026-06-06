import sympy as sp
x = sp.Symbol('x')
f_prime = 6*x**2 + 1
f = sp.integrate(f_prime, x) + 2
assert f.subs(x, 0) == 2, 'Initial condition failed'
result = f.subs(x, 1)
assert result == 5, f'Expected 5, got {result}'
print('VERIFY_PASS')