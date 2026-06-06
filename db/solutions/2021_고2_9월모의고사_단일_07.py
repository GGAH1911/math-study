import sympy as sp
a1, d = sp.symbols('a1 d')
eq1 = sp.Eq(2*a1 + 7*d, 25)
eq2 = sp.Eq(a1 + 7*d, 23)
sol = sp.solve([eq1, eq2], [a1, d])
a1_val, d_val = sol[a1], sol[d]
a4 = a1_val + 3*d_val
check1 = (a1_val + 2*d_val) + (a1_val + 5*d_val)
check2 = a1_val + 7*d_val
if check1 == 25 and check2 == 23 and a4 == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')