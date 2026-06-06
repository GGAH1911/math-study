from sympy import symbols, Eq, solve, simplify
x = symbols('x')
# 원래 방정식: 3^(4-x) = 9^(x-7)
# 9 = 3^2이므로: 3^(4-x) = 3^(2(x-7))
lhs = 3**(4-x)
rhs = 9**(x-7)
eq = Eq(lhs, rhs)
solution = solve(eq, x)
if 6 in solution:
    x_val = 6
    lhs_val = 3**(4-x_val)
    rhs_val = 9**(x_val-7)
    if abs(lhs_val - rhs_val) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')