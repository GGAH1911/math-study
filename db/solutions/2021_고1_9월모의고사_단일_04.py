from sympy import I, expand, re, im
result = expand((2 + 3*I) * (1 - I))
a = re(result)
b = im(result)
if a == 5 and b == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')