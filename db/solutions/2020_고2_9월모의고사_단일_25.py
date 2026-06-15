import math
from sympy import *

CANDIDATE = 4

# 주어진 조건
theta = symbols('theta', real=True)

# tan(theta) = -4/3, pi/2 < theta < pi
# 2사분면에서 sin > 0, cos < 0

# tan(theta) = sin(theta)/cos(theta) = -4/3
# sin(theta) = -4/3 * cos(theta)

# sin^2(theta) + cos^2(theta) = 1
# (16/9)*cos^2(theta) + cos^2(theta) = 1
# (25/9)*cos^2(theta) = 1
# cos^2(theta) = 9/25

# 2사분면: cos(theta) < 0
cos_theta = Rational(-3, 5)
sin_theta = Rational(4, 5)

# 검증: tan(theta) = -4/3
tan_check = sin_theta / cos_theta
assert tan_check == Rational(-4, 3), f"tan check failed: {tan_check}"

# 검증: sin^2 + cos^2 = 1
pythagorean_check = sin_theta**2 + cos_theta**2
assert pythagorean_check == 1, f"Pythagorean check failed: {pythagorean_check}"

# 원래 식 계산
# 5*sin(pi+theta) + 10*cos(pi/2-theta)
# = 5*(-sin(theta)) + 10*(sin(theta))
# = -5*sin(theta) + 10*sin(theta)
# = 5*sin(theta)

result = 5 * sin_theta
assert result == CANDIDATE, f"Result {result} does not match CANDIDATE {CANDIDATE}"

print('VERIFY_PASS')