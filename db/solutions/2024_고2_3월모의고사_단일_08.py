import sympy as sp
x, a, b = sp.symbols('x a b', real=True)

# Given conditions
a_val = 4
b_val = -8

# Check condition 1: vertical asymptote at x=4
assert a_val == 4, 'Asymptote condition failed'

# Check condition 2: passes through (2, 4)
y_at_2 = b_val / (2 - a_val)
assert y_at_2 == 4, f'Point condition failed: got {y_at_2}'

# Calculate answer
answer = a_val - b_val
assert answer == 12, f'Answer calculation failed: got {answer}'

print('VERIFY_PASS')