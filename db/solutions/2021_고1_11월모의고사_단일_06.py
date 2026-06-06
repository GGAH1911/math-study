from sympy import I, sqrt, expand
z = 2 + sqrt(2)*I
result = z**2 - 4*z
result_simplified = expand(result)
expected = -6
if result_simplified == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')