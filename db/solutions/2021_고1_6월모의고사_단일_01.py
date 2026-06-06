from sympy import I, simplify
result = 3*I + (1 - 2*I)
expected = 1 + I
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')