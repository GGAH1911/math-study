from math import comb
a = 4
coeff = comb(5, 2) * (2*a)**2
if coeff == 640:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')