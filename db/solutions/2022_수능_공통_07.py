from sympy import *
import math

# tan(theta) = 3
tan_theta = 3

# 제3사분면: sin < 0, cos < 0
cos_theta = -sqrt(10)/10
sin_theta = -3*sqrt(10)/10

# 검증 1: sin^2 + cos^2 = 1
verify1 = sin_theta**2 + cos_theta**2
print(f'sin²+cos²: {simplify(verify1)}')
assert simplify(verify1) == 1, 'VERIFY_FAIL: sin²+cos²≠1'

# 검증 2: tan(theta) = sin/cos = 3
verify2 = sin_theta / cos_theta
print(f'sin/cos: {simplify(verify2)}')
assert simplify(verify2) == 3, 'VERIFY_FAIL: tan≠3'

# 검증 3: tan(θ) - 6/tan(θ) = 1
verify3 = tan_theta - 6/tan_theta
print(f'tan-6/tan: {verify3}')
assert verify3 == 1, 'VERIFY_FAIL: condition not satisfied'

# 최종 답
result = sin_theta + cos_theta
print(f'sin(θ)+cos(θ): {simplify(result)}')
assert simplify(result) == -2*sqrt(10)/5, 'VERIFY_FAIL: answer incorrect'

print('VERIFY_PASS')