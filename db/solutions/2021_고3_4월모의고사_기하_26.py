import math
from math import sqrt

# 파라미터
p = 2
x0 = 6
y0 = 4 * sqrt(3)

# 포물선 확인: y^2 = 4px
assert abs(y0**2 - 4*p*x0) < 1e-10, 'parabola check failed'

# FA = 8 확인
FA = x0 + p
assert abs(FA - 8) < 1e-10, 'FA should be 8'

# 점들
F = (p, 0)
A = (x0, y0)
C = (0, y0)
B = (x0, 0)

# 삼각형 FBA 넓이
area_FBA = 0.5 * abs((B[0]-F[0]) * (A[1]-F[1]))
assert abs(area_FBA - 8*sqrt(3)) < 1e-10, 'FBA area should be 8√3'

# 사각형 OFAC 넓이 (신발끈 공식)
vertices_OFAC = [(0,0), (p, 0), (x0, y0), (0, y0)]
area_OFAC = 0.5 * abs(
    vertices_OFAC[0][0]*vertices_OFAC[1][1] - vertices_OFAC[1][0]*vertices_OFAC[0][1] +
    vertices_OFAC[1][0]*vertices_OFAC[2][1] - vertices_OFAC[2][0]*vertices_OFAC[1][1] +
    vertices_OFAC[2][0]*vertices_OFAC[3][1] - vertices_OFAC[3][0]*vertices_OFAC[2][1] +
    vertices_OFAC[3][0]*vertices_OFAC[0][1] - vertices_OFAC[0][0]*vertices_OFAC[3][1]
)
assert abs(area_OFAC / area_FBA - 2) < 1e-10, 'ratio should be 2:1'

# 삼각형 ACF 넓이
area_ACF = 0.5 * abs((C[0]-A[0])*(F[1]-A[1]) - (F[0]-A[0])*(C[1]-A[1]))
expected_area = 12 * sqrt(3)
assert abs(area_ACF - expected_area) < 1e-10, f'ACF area should be {expected_area}'

print('VERIFY_PASS')