import sympy as sp
from sympy import symbols, sin, cos, solve, pi, sqrt

theta = symbols('theta', real=True)

# 주어진 조건들
eq1 = sin(theta)*cos(theta) + 12/25  # sin(theta)cos(theta) = -12/25
eq2 = sin(theta)**2 + cos(theta)**2 - 1  # 항등식

# sin(theta) - cos(theta) = 7/5인지 검증하기 위해
# sin(theta)cos(theta) = -12/25를 만족하고 
# 제2사분면(π/2 < θ < π)에 속하는 θ를 찾음

# (sin θ - cos θ)^2 = sin²θ - 2sinθcosθ + cos²θ = 1 - 2sinθcosθ
square_result = 1 - 2*(-12/25)
print(f'(sin θ - cos θ)² = {square_result}')
print(f'(sin θ - cos θ)² = {float(square_result)}')

# 제2사분면에서 sinθ > 0, cosθ < 0이므로 sinθ - cosθ > 0
result = sqrt(square_result)
print(f'sin θ - cos θ = {result}')
print(f'sin θ - cos θ = {float(result)}')

# 검증: 실제로 이 조건을 만족하는 θ 존재 확인
# 25cos²θ + 35cosθ + 12 = 0으로부터
a, b, c = 25, 35, 12
discriminant = b**2 - 4*a*c
cos_vals = [(-b + sqrt(discriminant))/(2*a), (-b - sqrt(discriminant))/(2*a)]
print(f'\n가능한 cos θ 값들: {[float(v) for v in cos_vals]}')

for cos_val in cos_vals:
    sin_val = cos_val + result
    prod = sin_val * cos_val
    print(f'cos θ = {float(cos_val)}, sin θ = {float(sin_val)}, sinθcosθ = {float(prod)}')
    if abs(float(prod) - (-12/25)) < 1e-10:
        print('✓ 조건 만족')
        if 0 < float(sin_val) < 1 and -1 < float(cos_val) < 0:
            print('✓ 제2사분면 조건 만족')
            print('VERIFY_PASS')