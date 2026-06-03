import math
from sympy import *

# 주어진 조건: sin²θ = 4/5, θ는 제4사분면
sin_squared = Rational(4, 5)
cos_squared = 1 - sin_squared  # = 1/5

# 제4사분면: sin < 0, cos > 0
sin_theta = -sqrt(sin_squared)
cos_theta = sqrt(cos_squared)

# tan θ / cos θ 계산
tan_theta = sin_theta / cos_theta
result = tan_theta / cos_theta
result_simplified = simplify(result)

# 예상 답: -2√5
expected = -2*sqrt(5)

if simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')