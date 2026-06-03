from sympy import symbols, solve, expand
x = symbols('x')
f = lambda x_val: 2*x_val**2 + 4*x_val - 8
g = lambda x_val: x_val**3 - 6*x_val + 12
result = f(3)
assert result == 22, f'Expected 22, got {result}'
print('VERIFY_PASS')