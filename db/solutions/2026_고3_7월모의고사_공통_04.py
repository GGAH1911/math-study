from sympy import symbols, limit

a_val = 5
x = symbols('x')

# Left limit as x approaches 1 from left
f_left = 2*x + a_val
left_limit = limit(f_left, x, 1, '-')

# Right value at x = 1 (x >= 1 piece)
f_right = x**2 - a_val*x + 11
right_value = f_right.subs(x, 1)

# Check continuity
if left_limit == right_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')