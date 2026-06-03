from sympy import symbols, solve, Eq
a1, d = symbols('a1 d')
eq1 = Eq(a1 + 3*d, 6)
eq2 = Eq(2*(a1 + 6*d), a1 + 18*d)
sol = solve([eq1, eq2], [a1, d])
a1_val = sol[a1]
d_val = sol[d]
verify_a4 = a1_val + 3*d_val
verify_a7 = a1_val + 6*d_val
verify_a19 = a1_val + 18*d_val
if verify_a4 == 6 and 2*verify_a7 == verify_a19:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')