from math import comb

n = 8
coeff_x2 = comb(n, 2) * (2 ** (n - 2))
coeff_x3 = comb(n, 3) * (2 ** (n - 3))

if coeff_x2 == coeff_x3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')