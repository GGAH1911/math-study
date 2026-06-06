import sympy as sp
from sympy import symbols, sqrt, solve

x, y, b = symbols('x y b', real=True)

# Point B's intersection with line
point_B = (sp.Rational(6, 5), sp.Rational(8, 5))

# Circle C equation with b = 13/5
b_val = sp.Rational(13, 5)

# Verify point_B lies on circle C
lhs = (point_B[0] - b_val - 1)**2 + (point_B[1] - b_val)**2
rhs = b_val**2

print(f'LHS: {lhs}')
print(f'RHS: {rhs}')
print(f'Equal: {lhs == rhs}')

# Verify a < b
a_val = 1
print(f'\na = {a_val}, b = {b_val}')
print(f'a < b: {a_val < b_val}')
print(f'a + b = {a_val + b_val}')

if lhs == rhs:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')