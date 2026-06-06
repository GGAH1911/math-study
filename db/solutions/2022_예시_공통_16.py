from sympy import symbols, Eq, solve
a1, d = symbols('a1 d')
eq1 = Eq(a1 + 2*d, 7)
eq2 = Eq(2*a1 + 5*d, 16)
sol = solve([eq1, eq2], [a1, d])
a1_val, d_val = sol[a1], sol[d]
a10 = a1_val + 9*d_val
if a10 == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')