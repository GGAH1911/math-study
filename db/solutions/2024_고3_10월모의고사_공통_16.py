from sympy import *
x = symbols('x')
lhs = (Rational(1, 3))**x
rhs = 27**(x - 8)
result = solve(lhs - rhs, x)
if result:
    x_val = result[0]
    lhs_val = (Rational(1, 3))**x_val
    rhs_val = 27**(x_val - 8)
    if simplify(lhs_val - rhs_val) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')