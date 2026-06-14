from sympy import symbols, Eq, solve
a1, d = symbols('a1 d')
equation = Eq((a1 + d) + (a1 + 2*d), 2*(a1 + 12))
sol = solve(equation, d)
if sol and sol[0] == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')