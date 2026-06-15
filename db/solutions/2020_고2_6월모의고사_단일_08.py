import sympy as sp
a = sp.Symbol('a')
equation = sp.Eq(sp.log(9 - a, 2) + 1, 3)
sol = sp.solve(equation, a)
result = sol[0]
check = sp.log(9 - result, 2) + 1
if check == 3 and result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')