from sympy import sin, cos, sqrt, symbols, simplify, atan2, pi
import sympy as sp

# 파라미터 t 정의
t = symbols('t', real=True)

# 곡선 방정식
x = sin(t) - cos(t)
y = 3*cos(t) + sin(t)

# 미분
dx_dt = cos(t) + sin(t)
dy_dt = -3*sin(t) + cos(t)

# 기울기
slope = dy_dt / dx_dt

# 기울기 = 3 조건
# -3*sin(t) + cos(t) = 3*(cos(t) + sin(t))
# -3*sin(t) + cos(t) = 3*cos(t) + 3*sin(t)
# -6*sin(t) = 2*cos(t)
# tan(t) = -1/3

# 0 < t < π이고 tan(t) = -1/3인 경우 (제2사분면)
sin_t = 1/sqrt(10)
cos_t = -3/sqrt(10)

# 점 (a, b) 계산
a = sin_t - cos_t
b = 3*cos_t + sin_t

# 정답
result = simplify(a + b)

# 검증: 기울기가 3인지 확인
slope_check = slope.subs([(sin(t), sin_t), (cos(t), cos_t)])
slope_check_simplified = simplify(slope_check)

# 최종 검사
if simplify(slope_check_simplified - 3) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')