from sympy import symbols, Eq, solve
a1, d = symbols('a1 d')
eq1 = Eq(a1 + 2*d, 2)
eq2 = Eq(a1 + 6*d, 62)
sol = solve([eq1, eq2], [a1, d])
a1_val, d_val = sol[a1], sol[d]
a5 = a1_val + 4*d_val
verify1 = a1_val + 2*d_val == 2
verify2 = a1_val + 6*d_val == 62
if verify1 and verify2 and a5 == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')