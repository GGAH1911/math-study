import sympy as sp
from sympy import sin, cos, tan, pi, sqrt, simplify

theta = sp.Symbol('theta', real=True)

# 주어진 조건 검증
# tan(π - θ) = -2
tan_condition = tan(pi - theta) + 2  # = 0 이어야 함

# tan(π - θ) = -tan(θ) 이므로 tan(θ) = 2
# 우리의 답: cos(θ) = -√5/5, sin(θ) = -2√5/5

cos_theta = -sqrt(5)/5
sin_theta = -2*sqrt(5)/5

# 검증 1: sin²θ + cos²θ = 1
verify1 = simplify(sin_theta**2 + cos_theta**2)
print(f'sin²θ + cos²θ = {verify1}')
assert verify1 == 1, 'Identity check failed'

# 검증 2: tan(θ) = 2
tan_theta = simplify(sin_theta / cos_theta)
print(f'tan(θ) = {tan_theta}')
assert tan_theta == 2, 'tan(θ) check failed'

# 검증 3: tan(π - θ) = -2
tan_pi_minus_theta = -tan_theta  # tan(π - θ) = -tan(θ)
print(f'tan(π - θ) = {tan_pi_minus_theta}')
assert tan_pi_minus_theta == -2, 'tan(π - θ) check failed'

# 최종 답
answer = simplify(cos_theta - sin_theta)
print(f'cos(θ) - sin(θ) = {answer}')
assert answer == sqrt(5)/5, 'Final answer check failed'

print('VERIFY_PASS')