from sympy import *
a = Rational(4, 3)
b = 4
# 점근선의 기울기는 b/a
slope = b / a
if slope == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')