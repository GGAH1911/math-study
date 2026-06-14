import sympy as sp
from sympy import sqrt, sin, cos, tan, atan2, pi

CANDIDATE = 80

# 점 P의 좌표 설정 (a, b), a = 2*sqrt(2)*b 관계식 확인
b_sym = sp.Symbol('b', positive=True, real=True)
a_sym = 2*sqrt(2)*b_sym

# 원점에서의 거리
dist_OP = sqrt(a_sym**2 + b_sym**2)

# sin(alpha) 계산
sin_alpha = b_sym / dist_OP
sin_alpha_simplified = sp.simplify(sin_alpha)

# sin(alpha) = 1/3인지 확인
assert sp.simplify(sin_alpha_simplified - sp.Rational(1,3)) == 0, "sin(alpha) should be 1/3"

# 점 Q의 좌표 (b, a)
# sin(beta) 계산
sin_beta = a_sym / dist_OP
sin_beta_simplified = sp.simplify(sin_beta)
sin_beta_squared = sp.simplify(sin_beta_simplified**2)

# cos(beta) 계산 (Q는 제1사분면)
cos_beta_squared = 1 - sin_beta_squared
cos_beta_squared_simplified = sp.simplify(cos_beta_squared)

# tan(beta) 계산
tan_beta_squared = sin_beta_squared / cos_beta_squared_simplified
tan_beta_squared_simplified = sp.simplify(tan_beta_squared)

# 점 R의 좌표 (-b, -a)
# sin(gamma), cos(gamma) 계산 (R은 제3사분면)
sin_gamma = -a_sym / dist_OP
cos_gamma = -b_sym / dist_OP

tan_gamma = sin_gamma / cos_gamma
tan_gamma_simplified = sp.simplify(tan_gamma)
tan_gamma_squared = sp.simplify(tan_gamma_simplified**2)

# 최종 값 계산
result = 9 * (sin_beta_squared + tan_gamma_squared)
result_simplified = sp.simplify(result)

if result_simplified == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {CANDIDATE}, got {result_simplified}")