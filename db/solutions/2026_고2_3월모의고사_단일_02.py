from sympy import I, expand
result = (2 + I) * (2 - I)
print('VERIFY_PASS' if expand(result) == 5 else 'VERIFY_FAIL')