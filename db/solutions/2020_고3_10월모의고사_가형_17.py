import math
from sympy import symbols, solve, sqrt, simplify

# 좌표 설정
A = (0, 12)
D = (4, 0)
C = (9, 0)

# 외접원의 중심 구하기
# |O'A|^2 = |O'D|^2 => x - 3y = -16
# |O'D|^2 = |O'C|^2 => x = 6.5
x_c = 6.5
y_c = (6.5 + 16) / 3

# 반지름 제곱
R_squared = (x_c - D[0])**2 + (y_c - D[1])**2

# 세 점으로부터의 거리 확인
dist_A_sq = (x_c - A[0])**2 + (y_c - A[1])**2
dist_D_sq = (x_c - D[0])**2 + (y_c - D[1])**2
dist_C_sq = (x_c - C[0])**2 + (y_c - C[1])**2

# 넓이 계산
area = math.pi * R_squared
target_area = (125/2) * math.pi

if abs(R_squared - 62.5) < 1e-9 and abs(area - target_area) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')