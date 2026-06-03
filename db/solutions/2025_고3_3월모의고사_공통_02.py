import sympy as sp
x, h = sp.symbols('x h')
f = x**3 - 4*x**2 + x
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 3)
expected = 4
assert result == expected, f'Expected {expected}, got {result}'
print('VERIFY_PASS')