import sympy as sp
from sympy import sqrt, simplify

# 주어진 조건: sec(theta) = sqrt(10)/3
sec_theta = sqrt(10) / 3

# cos(theta) = 1/sec(theta)
cos_theta = 1 / sec_theta
cos_theta = simplify(cos_theta)

# cos^2(theta) 계산
cos2_theta = cos_theta ** 2
cos2_theta = simplify(cos2_theta)

# sin^2(theta) = 1 - cos^2(theta)
sin2_theta = 1 - cos2_theta
sin2_theta = simplify(sin2_theta)

# 정답 검증: sin^2(theta)가 1/10인지 확인
answer = sp.Rational(1, 10)
if simplify(sin2_theta - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')