from sympy import log, simplify
result = 4 ** (log(3, 2))
simplified = simplify(result)
if simplified == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')