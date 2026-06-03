from sympy import symbols, summation
k = symbols('k', integer=True)
sum1 = summation(k**2 + 2*k - 4, (k, 1, 5))
sum2 = summation(2*k + 5, (k, 1, 5))
result = sum1 - sum2
if result == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')