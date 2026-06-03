from fractions import Fraction

n = 80
p = Fraction(1, 8)
EX = n * p

if EX == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')