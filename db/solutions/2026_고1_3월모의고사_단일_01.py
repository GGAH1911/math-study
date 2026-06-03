from fractions import Fraction
a = Fraction(4, 3)
b = Fraction(-1, 3)
c = Fraction(-1, 9)
result = (a - b) / c
answer = -15
if result == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')