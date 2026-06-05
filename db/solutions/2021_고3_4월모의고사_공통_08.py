from sympy import symbols, limit, simplify, expand
x, a, b = symbols('x a b')
f_left = (x**2 + 3*x + a)/(x - 2)
f_right = -x**2 + b
a_val = -10
b_val = 11
left_lim = limit(f_left.subs(a, a_val), x, 2, '-')
right_val = -(2)**2 + b_val
if left_lim == right_val:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {left_lim} != {right_val}')