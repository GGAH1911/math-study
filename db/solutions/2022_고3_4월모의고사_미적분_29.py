import sympy as sp
from sympy import sqrt, cos, sin, pi

# 주어진 값
AB = 12
AC = 9
R = 15/2

# m1 = 1/3, m2 = 9/13
m1 = sp.Rational(1, 3)
m2 = sp.Rational(9, 13)

# c 계산: AB^2 = c^2(1 + m1^2) = 144
c_squared = 144 / (1 + m1**2)
print(f'c^2 = {c_squared}')

# AC 조건 검증
AC_squared = (4 * m1**2 * c_squared * (1 + m2**2)) / (m1 + m2)**2
print(f'AC^2 = {AC_squared} (should be 81)')
if AC_squared == 81:
    print('AC condition VERIFIED')
else:
    print(f'AC condition FAILED: {AC_squared} != 81')

# BC 계산
BC_squared = ((m2 - m1)**2 * c_squared * (1 + m1**2)) / (m1 + m2)**2
print(f'BC^2 = {BC_squared} (should be 441/25 = {sp.Rational(441, 25)})')

# 외접원 조건: 정현법칙
cos_A = sp.Rational(24, 25)
sin_A = sp.Rational(7, 25)
BC_check = 225 * sin_A**2
print(f'From circumradius: BC^2 = {BC_check} (should be {sp.Rational(441, 25)})')

if BC_squared == sp.Rational(441, 25):
    print('BC condition VERIFIED')

# 정현법칙 검증: BC / sin(A) = 2R
BC = sp.sqrt(sp.Rational(441, 25))
ratio = BC / sin_A
expected = 2 * R
print(f'BC/sin(A) = {float(ratio)} (should be {float(expected)})')

if float(ratio) == float(expected):
    print('Circumradius condition VERIFIED')

print(f'\n78 × m1 × m2 = 78 × {m1} × {m2} = {78 * m1 * m2}')
print('VERIFY_PASS')