from sympy import I, re, im
result = 2 / (1 - I)
a = re(result)
b = im(result)
verification = (a + b) == 2
print('VERIFY_PASS' if verification else 'VERIFY_FAIL')