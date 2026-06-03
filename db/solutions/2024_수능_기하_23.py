from sympy import symbols, solve, Eq
a, b = symbols('a b')
eq1 = Eq((a + 9) / 2, 4)
eq2 = Eq((-2 + 2) / 2, 0)
eq3 = Eq((6 + b) / 2, 7)
a_val = solve(eq1, a)[0]
b_val = solve(eq3, b)[0]
result = a_val + b_val
if result == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')