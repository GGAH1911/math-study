from sympy import I
z1 = 1 + I
z2 = 3 - 4*I
result = z1 + z2
expected = 4 - 3*I
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')