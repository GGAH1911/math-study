from sympy import log, simplify, N
result = log(18, 3) - log(2, 3)
verify_value = simplify(result)
if verify_value == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')