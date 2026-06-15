import sympy as sp
val = sp.log(4, 10) + sp.log(25, 10)
val = sp.simplify(val)
if val == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')