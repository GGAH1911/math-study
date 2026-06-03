import sympy as sp
from sympy import sqrt, sin, cos, tan, pi, simplify

# 주어진 조건: pi/2 < theta < pi, tan(theta) = -2
# tan(theta) = -2에서 sin(theta) = -2*cos(theta)
# sin^2(theta) + cos^2(theta) = 1 사용

# cos(theta) 구하기
# 5*cos^2(theta) = 1이므로 cos^2(theta) = 1/5
# 제2사분면에서 cos(theta) < 0
cos_theta = -1/sqrt(5)
sin_theta = -2 * cos_theta

# 검증
assert simplify(sin_theta**2 + cos_theta**2) == 1
assert simplify(sin_theta / cos_theta) == -2
assert sin_theta > 0  # 제2사분면에서 양수
assert cos_theta < 0  # 제2사분면에서 음수

# sin(pi + theta) = -sin(theta) 계산
result = -sin_theta
result_simplified = simplify(result)
expected = -2*sqrt(5)/5

if simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')