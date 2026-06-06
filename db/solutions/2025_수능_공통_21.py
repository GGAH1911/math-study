import sympy as sp
x = sp.Symbol('x')
a, b = 4, 7
f = x**3 + a*x**2 + b*x + 4
result_at_1 = f.subs(x, 1)
print(f'f(1) = {result_at_1}')
assert result_at_1 == 16, f'Expected 16, got {result_at_1}'
factored = sp.factor(f)
print(f'f(x) factored: {factored}')
q = x**2 + (a-1)*x + 4
discriminant = (a-1)**2 - 16
print(f'Discriminant of q(x): {discriminant}')
assert discriminant < 0, 'q(x) must have no real roots'
print('VERIFY_PASS')