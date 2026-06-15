import sympy as sp
from sympy import sqrt, simplify, symbols

# 쌍곡선과 원의 교점 구하기
x = sp.Symbol('x', positive=True, real=True)
y = sp.Symbol('y', positive=True, real=True)

# P가 만족하는 조건들
# 1) 쌍곡선: x^2/4 - y^2/12 = 1
# 2) 원: x^2 + y^2 = 16
# 3) 각도 조건: PA·PB = 0

# x^2 + y^2 = 16에서 y^2 = 16 - x^2
# 쌍곡선에 대입
eq = sp.Eq(x**2/4 - (16-x**2)/12, 1)
x_val = sp.solve(eq, x)
x_coord = [val for val in x_val if val > 0][0]
y_coord = sqrt(16 - x_coord**2)

# P의 좌표
P = (x_coord, y_coord)

# 직선 AP: A=(-4,0), P=(√7, 3)
# 직선의 방정식: 3x - (√7+4)y + 12 = 0

# 원점에서 직선까지의 거리
A = (-4, 0)
slope_coeff = sqrt(7) + 4
numerator = abs(12)
denominator = sqrt(9 + slope_coeff**2)

dist = numerator / denominator
dist_simplified = simplify(dist)

# 답 값
answer_value = sqrt(7) - 1

if simplify(dist_simplified - answer_value) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed {dist_simplified}, expected {answer_value}')