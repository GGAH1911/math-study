from sympy import symbols, Eq, solve
a1 = symbols('a1')
eq = Eq(a1 * 27, 24)
a1_val = solve(eq, a1)[0]
a3_val = a1_val * 9
print('VERIFY_PASS' if a3_val == 8 else 'VERIFY_FAIL')