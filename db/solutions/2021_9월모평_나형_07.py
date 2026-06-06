from sympy import symbols, solve, Eq
a1, d = symbols('a1 d')
eq1 = Eq(d, 3)
eq2 = Eq((a1 + 2*d) + (a1 + 6*d), 64)
sol = solve([eq1, eq2], [a1, d])
if sol:
    a1_val, d_val = sol[a1], sol[d]
    a2 = a1_val + (2-1)*d_val
    a3 = a1_val + (3-1)*d_val
    a7 = a1_val + (7-1)*d_val
    check = a3 + a7
    if check == 64 and a2 == 23:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')