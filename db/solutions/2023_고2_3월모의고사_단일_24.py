from sympy import symbols, expand, div
x = symbols('x')
P = 3*x**3 + x**2 + 10*x + 8
remainder_value = P.subs(x, 1)
assert remainder_value == 22, f'Expected 22, got {remainder_value}'
print('VERIFY_PASS')