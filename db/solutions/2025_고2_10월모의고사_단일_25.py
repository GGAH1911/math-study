from sympy import symbols, Eq, solve

a, d = symbols('a d')
eq1 = Eq(a + 4*d, 3)
eq2 = Eq(11*(a + 5*d), 88)
sol = solve([eq1, eq2], [a, d])
a_val, d_val = sol[a], sol[d]

a_7 = a_val + 6*d_val
if a_7 == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')