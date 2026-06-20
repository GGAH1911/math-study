from sympy import *
x = symbols('x', real=True)

# Define f(x) piecewise
f = Piecewise((x**2 + 1, x <= 1), (3*x - 1, x > 1))

# Compute integral
result = integrate(x**2 + 1, (x, 0, 1)) + integrate(3*x - 1, (x, 1, 2))
print(f'Integral result: {result}')
print(f'Simplified: {simplify(result)}')

# Verify conditions at key points
print(f'\nVerifying conditions:')
for test_x in [0, 0.5, 1, 1.5, 2]:
    if test_x <= 1:
        f_val = test_x**2 + 1
        g_val = 3*test_x - 1
    else:
        f_val = 3*test_x - 1
        g_val = test_x**2 + 1
    
    sum_check = f_val + g_val
    prod_check = f_val * g_val
    expected_sum = test_x**2 + 3*test_x
    expected_prod = (test_x**2 + 1) * (3*test_x - 1)
    
    print(f'x={test_x}: f+g={sum_check} (expected {expected_sum}), f*g={prod_check} (expected {expected_prod}), f≥g: {f_val >= g_val}')

if result == Rational(29, 6):
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')