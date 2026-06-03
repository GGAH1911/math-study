from fractions import Fraction

p = Fraction(1, 3)
n = 18

E_X = n * p
E_3X_minus_1 = 3 * E_X - 1
V_X = n * p * (1 - p)

if E_3X_minus_1 == 17 and V_X == 4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: E(3X-1)={E_3X_minus_1}, V(X)={V_X}')
