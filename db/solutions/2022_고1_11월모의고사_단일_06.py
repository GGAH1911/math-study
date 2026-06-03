from sympy import symbols, expand, Eq, solve
x, a, b = symbols('x a b')
lhs = 2*x**2 + a*x + 1
rhs = (b*x + 1)*(x + 1)
rhs_expanded = expand(rhs)
eq = Eq(lhs - rhs_expanded, 0)
coeffs_lhs = [2, a, 1]
coeffs_rhs = [b, b+1, 1]
result = solve([Eq(2, b), Eq(a, b+1)], [a, b])
if result[a] == 3 and result[b] == 2:
    test_lhs = 2*x**2 + 3*x + 1
    test_rhs = expand((2*x + 1)*(x + 1))
    if test_lhs == test_rhs:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')