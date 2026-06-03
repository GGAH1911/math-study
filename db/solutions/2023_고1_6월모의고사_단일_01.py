from sympy import I, expand, simplify
result = I * (1 - I)
result = expand(result)
expected = 1 + I
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')