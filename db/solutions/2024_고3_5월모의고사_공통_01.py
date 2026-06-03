import sympy as sp
sqrt3 = sp.sqrt(3)
expr = 4**(1-sqrt3) * 2**(1+2*sqrt3)
result = sp.simplify(expr)
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')