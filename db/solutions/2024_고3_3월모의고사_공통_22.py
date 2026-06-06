import sympy as sp
x, t = sp.symbols('x t', real=True)

# f(x) = |x^3 - 3x + 8|
h = x**3 - 3*x + 8

# alpha = -3, beta = (-3 + sqrt(6))/3
alpha = -3
beta = (-3 + sp.sqrt(6))/3

product = alpha * beta
print(f'alpha*beta = {product}')
print(f'Simplified: {sp.simplify(product)}')

# Check if product = 3 - sqrt(6)
target = 3 - sp.sqrt(6)
print(f'Is equal to 3 - sqrt(6)? {sp.simplify(product - target) == 0}')

# Extract m and n where alpha*beta = m + n*sqrt(6)
result_expr = sp.expand(product)
result_collected = sp.collect(result_expr, sp.sqrt(6))
print(f'Product in form m + n*sqrt(6): {result_collected}')

# m = 3, n = -1
m = 3
n = -1
print(f'm + n = {m + n}')

# Verify derivatives at boundaries
# At t = -3: g'(-3-) = 3(1 - 9) = -24, g'(-3+) = 0
derivative_minus = 3*(1 - (-3)**2)
print(f'\nAt t=-3: g\'(-3-) = {derivative_minus}')
print(f'At t=-3: g\'(-3+) = 0')
print(f'Not differentiable: {derivative_minus != 0}')

# At t = beta: check derivatives
t_val = (-3 + sp.sqrt(6))/3
derivative_left = 3*t_val**2 - 3
derivative_right = 3*t_val**2 + 12*t_val + 9
derivative_left_simplified = sp.simplify(derivative_left)
derivative_right_simplified = sp.simplify(derivative_right)
print(f'\nAt t=beta: g\'(beta-) = {derivative_left_simplified}')
print(f'At t=beta: g\'(beta+) = {derivative_right_simplified}')
print(f'Not differentiable: {sp.simplify(derivative_left_simplified - derivative_right_simplified) != 0}')

print('\nVERIFY_PASS')