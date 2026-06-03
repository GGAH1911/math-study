from sympy import sqrt, symbols, simplify
x = (3 + sqrt(13))/2
result = x**2 - 3*x - 1
if simplify(result) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')