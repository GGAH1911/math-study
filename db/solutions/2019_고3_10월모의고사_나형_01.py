import sympy as sp
val = sp.log(24, 2) - sp.log(3, 2)
val = sp.simplify(val)
if val == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')