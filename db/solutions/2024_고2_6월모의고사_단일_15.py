import sympy as sp
from sympy import sqrt, cos, sin, symbols, solve

# 변수 정의
r_val = 2*sqrt(13)/3

# 원 위의 점들
# x = -2일 때 y = ±sqrt(r^2 - 4)
y_val = sqrt(r_val**2 - 4)

# 점 A, B의 좌표
A_x, A_y = -2, y_val
B_x, B_y = -2, -y_val

# 각도 계산
cos_alpha = A_x / r_val
sin_alpha = A_y / r_val
cos_beta = B_x / r_val
sin_beta = B_y / r_val

# 조건 검증: 2*cos(alpha) = 3*sin(beta)
cond_check = 2*cos_alpha - 3*sin_beta
cond_simplified = sp.simplify(cond_check)

# 최종 계산
result = r_val * (sin_alpha + cos_beta)
result_simplified = sp.simplify(result)

# 검증
if sp.simplify(result_simplified + sp.Rational(2, 3)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')