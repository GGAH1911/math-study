from sympy import cbrt, simplify
expr = cbrt(5) * cbrt(25)
result = simplify(expr)
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')