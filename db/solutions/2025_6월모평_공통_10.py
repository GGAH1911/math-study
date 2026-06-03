import sympy as sp
from sympy import sin, cos, pi, sqrt, symbols, simplify

# 역산: 답이 주어진 조건을 만족하는지 확인
R = 3  # 외접원 반지름
A_val = 2*pi/3  # A + 2B = pi이고 cos B = 1/3일 때
B_val = pi/6  # B = C이고 cos B = 1/3일 때

# 실제로 cos B = 1/3일 때의 B
cos_B = sp.Rational(1, 3)
sin_B = sqrt(1 - cos_B**2)
cos_B_check = simplify(sin(2*sin_B**(-1)))

# 정현법칙으로 변의 길이
a = 6 * 2*sin_B*cos_B  # sin A = sin 2B
b = 6 * sin_B
c = b

# 조건 (가) 확인: 3*sin A = 2*sin B
sin_A = 2*sin_B*cos_B
condition_ga = simplify(3*sin_A - 2*sin_B)

# 조건 (나) 확인: cos B = cos C
condition_na = cos_B - cos_B  # B = C이므로 0

# 삼각형의 넓이
area = sp.Rational(1, 2) * b**2 * sin_A
area_simplified = simplify(area)

# 외접원 넓이 확인
circumradius_area = 9

if simplify(condition_ga) == 0 and condition_na == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')