from fractions import Fraction
a = Fraction(1, 4)
r = 2
a5 = a * (r ** 4)
a6 = a * (r ** 5)
a7 = a * (r ** 6)
a8 = a * (r ** 7)
cond1 = (a5 == 4)
cond2 = (a7 == 4 * a6 - 16)
if cond1 and cond2 and a8 == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')