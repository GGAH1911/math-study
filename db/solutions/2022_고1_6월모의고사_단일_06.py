from sympy import symbols, expand
a = 101
result = a**3 - 3*(a**2) + 3*a - 1
expected = 100**3
if result == expected == 10**6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')