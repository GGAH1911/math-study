from sympy import symbols, log, solve
a = symbols('a')
expr = a + log(4, 2) - 7
sol = solve(expr, a)
print('VERIFY_PASS' if sol and sol[0] == 5 else 'VERIFY_FAIL')