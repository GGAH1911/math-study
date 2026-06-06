import sympy as sp
x = sp.Symbol('x')
f_prime = 8*x**3 - 12*x**2 + 7
f = sp.integrate(f_prime, x) + 3
assert f.subs(x, 0) == 3, 'Initial condition failed'
result = f.subs(x, 1)
assert result == 8, f'f(1) should be 8, got {result}'
print('VERIFY_PASS')