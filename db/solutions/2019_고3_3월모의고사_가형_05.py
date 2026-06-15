from sympy import *
x, a, b = symbols('x a b', real=True)
# f(y) = ln(x - a) + b, asymptote at x=1 => a=1
a_val = 1
# passes through (2, 5)
b_val = solve(ln(2 - a_val) + b - 5, b)[0]
result = a_val + b_val
print('a =', a_val, ', b =', b_val, ', a+b =', result)
# Verify asymptote
func = ln(x - a_val) + b_val
asymptote_check = limit(func, x, a_val, '+')
pass_asymptote = asymptote_check == -oo
pass_point = Eq(func.subs(x, 2), 5)
if pass_asymptote and pass_point and result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')