from sympy import symbols, cos, solve, Eq
import math

# 변의 길이
a, b, c = 2, 3, 4

# 코사인 법칙: c^2 = a^2 + b^2 - 2ab*cos(C)
# c^2 - a^2 - b^2 = -2ab*cos(C)
# cos(C) = (a^2 + b^2 - c^2) / (2ab)

cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
print(f'cos C = {cos_C}')
print(f'cos C = {cos_C} = {int(cos_C * 4)}/4')

# 검증: cos C = -1/4
candidate = -1/4
computed = (a**2 + b**2 - c**2) / (2 * a * b)

if abs(computed - candidate) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')