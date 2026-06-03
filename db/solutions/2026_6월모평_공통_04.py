from sympy import symbols, solve, limit, oo
x, a = symbols('x a')
f_left = -x**2 + a
f_right = 5*x - a
limit_left_at_3 = limit(f_left, x, 3, '-')
limit_right_at_3 = f_right.subs(x, 3)
a_value = 12
result_left = limit_left_at_3.subs(a, a_value)
result_right = limit_right_at_3.subs(a, a_value)
if result_left == result_right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')