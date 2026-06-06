from sympy import symbols, expand, solve
x, a, b = symbols('x a b')
eq = x**2 + a*x - 4
roots_product = (-4) * b
roots_sum = -4 + b
eq_val = x**2 + 3*x - 4
roots = solve(eq_val, x)
result = a + b
ans_a, ans_b = 3, 1
check_product = (-4) * ans_b == -4
check_sum = -4 + ans_b == -ans_a
check_roots = set(solve(x**2 + ans_a*x - 4, x)) == {-4, ans_b}
if check_product and check_sum and check_roots:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')