import sympy as sp
a1, r = 4, 2
a4 = a1 * (r ** 3)
a2 = a1 * r
a5 = a1 * (r ** 4)
check1 = (a4 == 4 * a2)
check2 = (a1 + a2 == 12)
check3 = (a5 == 64)
if check1 and check2 and check3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')