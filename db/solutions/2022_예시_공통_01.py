import sympy as sp
sqrt5 = sp.sqrt(5)
exponent = (sqrt5 + 1) - (sqrt5 - 1)
result = 3 ** exponent
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')