from sympy import symbols, sin, cos, tan, pi, atan, simplify, solve, sqrt
from sympy import Rational as R

# α의 값 설정
alpha = atan(R(-5, 12))
alpha_val = -atan(R(5, 12)) + 2*pi  # 4사분면

sin_alpha = R(-5, 13)
cos_alpha = R(12, 13)

# tan x의 범위
tan_min = R(3, 2)
tan_max = R(31, 12)

# 합 계산
sum_val = tan_min + tan_max
print(f'최솟값: {tan_min}')
print(f'최댓값: {tan_max}')
print(f'합: {sum_val}')

# 검증: tan x = 3/2일 때
x1 = atan(R(3, 2))
sin_x1 = sin(x1)
cos_x1 = cos(x1)
sin_xalpha1 = sin_x1 * cos_alpha + cos_x1 * sin_alpha
sin_xalpha1 = simplify(sin_xalpha1)

check1_left = simplify(cos_x1 - sin_xalpha1) <= 0
check1_right = simplify(sin_xalpha1 - 2*cos_x1) <= 0

print(f'\ntan x = 3/2 검증:')
print(f'  cos x = sin(x+α): {simplify(cos_x1 - sin_xalpha1) == 0}')
print(f'  sin(x+α) ≤ 2cos x: {check1_right}')

# 검증: tan x = 31/12일 때
x2 = atan(R(31, 12))
sin_x2 = sin(x2)
cos_x2 = cos(x2)
sin_xalpha2 = sin_x2 * cos_alpha + cos_x2 * sin_alpha
sin_xalpha2 = simplify(sin_xalpha2)

check2_left = simplify(cos_x2 - sin_xalpha2) <= 0
check2_right = simplify(sin_xalpha2 - 2*cos_x2) <= 0

print(f'\ntan x = 31/12 검증:')
print(f'  cos x ≤ sin(x+α): {check2_left}')
print(f'  sin(x+α) = 2cos x: {simplify(sin_xalpha2 - 2*cos_x2) == 0}')

if check1_left and check1_right and check2_left and check2_right:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')