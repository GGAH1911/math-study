from sympy import symbols, Eq, solve
a1, d = symbols('a1 d')
eq1 = Eq(a1, 4)
eq2 = Eq((a1 + 9*d) - (a1 + 6*d), 6)
sol = solve([eq1, eq2], [a1, d])
a_1 = sol[a1]
d_val = sol[d]
a_4 = a_1 + 3*d_val
if a_4 == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')