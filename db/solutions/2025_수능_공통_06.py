import math
from sympy import *

# 주어진 조건: cos(π/2 + θ) = -1/5
# 이를 만족하는 θ 찾기
theta_sym = symbols('theta', real=True)

# cos(π/2 + θ) = -sin(θ) = -1/5
# 따라서 sin(θ) = 1/5
sin_theta = Rational(1, 5)

# 피타고라스 정리로 cos²θ 구하기
# sin²θ + cos²θ = 1
cos_squared = 1 - sin_theta**2

# 검증: 주어진 조건 확인
# cos(π/2 + θ) = -sin(θ) = -1/5
cos_condition = -sin_theta
assert cos_condition == -Rational(1, 5), f"조건 불만족: {cos_condition}"

# 구하는 식: sin(θ) / (1 - cos²θ)
numerator = sin_theta
denominator = 1 - cos_squared  # = sin²θ
result = numerator / denominator

print(f"sin(θ) = {sin_theta}")
print(f"1 - cos²(θ) = sin²(θ) = {denominator}")
print(f"결과 = {sin_theta} / {denominator} = {result}")

if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')