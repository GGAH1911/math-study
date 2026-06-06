import sympy as sp
from sympy import sqrt, symbols, simplify

# 구한 답: p = 3, r = 9
p, r = 3, 9

# 각 점의 좌표
A = (p + r, 0)
P = (r - p, 2*sqrt(p*(r-p)))
H = (-p, 2*sqrt(p*(r-p)))
F = (p, 0)

# 1. P가 포물선 y^2 = 4px 위에 있는지 확인
y_P = 2*sqrt(p*(r-p))
parabola_check = y_P**2 - 4*p*(r-p)
print(f'포물선 확인: {simplify(parabola_check) == 0}')

# 2. P가 원 (x-p)^2 + y^2 = r^2 위에 있는지 확인
x_P = r - p
circle_check = (x_P - p)**2 + y_P**2 - r**2
print(f'원 확인: {simplify(circle_check) == 0}')

# 3. cos(∠PHF) = √3/3 확인
vec_HP = (P[0] - H[0], P[1] - H[1])
vec_HF = (F[0] - H[0], F[1] - H[1])
dot_product = vec_HP[0]*vec_HF[0] + vec_HP[1]*vec_HF[1]
mag_HP = sqrt(vec_HP[0]**2 + vec_HP[1]**2)
mag_HF = sqrt(vec_HF[0]**2 + vec_HF[1]**2)
cos_angle = simplify(dot_product / (mag_HP * mag_HF))
expected_cos = sqrt(3)/3
print(f'각도 확인: {simplify(cos_angle - expected_cos) == 0}')

# 4. 사각형 APHF의 넓이 = 54√2 확인
from sympy import Polygon
poly_area = abs((A[0]*(P[1]-F[1]) + P[0]*(H[1]-A[1]) + H[0]*(F[1]-P[1]) + F[0]*(A[1]-H[1])) / 2)
area_simplified = simplify(poly_area)
expected_area = 54*sqrt(2)
print(f'넓이 확인: {simplify(area_simplified - expected_area) == 0}')

if all([simplify(parabola_check) == 0, simplify(circle_check) == 0, 
        simplify(cos_angle - expected_cos) == 0, simplify(area_simplified - expected_area) == 0]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')