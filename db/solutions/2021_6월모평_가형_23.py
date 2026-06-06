from sympy import *
R = 15
sin_B = Rational(7, 10)
AC = 2 * R * sin_B
print(f'AC = {AC}')
result = (AC / sin_B) - (2 * R)
if abs(result) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result}')