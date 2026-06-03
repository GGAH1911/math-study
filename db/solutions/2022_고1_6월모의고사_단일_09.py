from sympy import I, expand
x = 2 + I
y = 2 - I
result = x**4 + x**2 * y**2 + y**4
result_simplified = expand(result)
if result_simplified == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')