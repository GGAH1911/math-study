import sympy as sp
from sympy import sqrt, sin, cos, pi, simplify, Rational

# sin(theta) 구하기
sin_theta = sqrt(Rational(6, 7))
cos_theta = sqrt(1 - Rational(6, 7))

# 삼각형 넓이로 검증
area = Rational(1, 2) * 2 * sqrt(7) * sin_theta
assert simplify(area - sqrt(6)) == 0, f'Area check failed: {area}'

# sin(pi/2 + theta) = cos(theta)
result = cos_theta
expected = sqrt(7) / 7

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')