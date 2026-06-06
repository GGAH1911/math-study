import sympy as sp
a, b = sp.symbols('a b')
eq1 = sp.Eq(20*a + 5*b, 360)
eq2 = sp.Eq(15*a + 25*b, 440)
sol = sp.solve([eq1, eq2], [a, b])
if sol[a] == 16 and sol[b] == 8:
    result = sol[a] + sol[b]
    if result == 24:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')