from sympy import symbols, expand
x, y = symbols('x y')
expr = (2*x + y)**3
expanded = expand(expr)
print(f'Expanded form: {expanded}')
coeff_xy2 = expanded.coeff(x*y**2)
print(f'Coefficient of xy^2: {coeff_xy2}')
assert coeff_xy2 == 6, f'Expected 6, got {coeff_xy2}'
print('VERIFY_PASS')