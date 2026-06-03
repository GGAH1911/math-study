from sympy import *

a_val = Rational(1, 2)

# 연속 조건: |a - 4| = |a + 3|
left_abs = abs(a_val - 4)
right_abs = abs(a_val + 3)

if left_abs == right_abs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')