import sympy as sp
import math

k = sp.Rational(4, 3)

# 원의 중심과 반지름
center_x, center_y = -1, 0
radius = 2

# 직선 kx + y - 2 = 0에서 중심까지의 거리
numerator = abs(k * center_x + center_y - 2)
denominator = sp.sqrt(k**2 + 1)
distance = numerator / denominator

# 반지름과 비교
if distance == radius:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Distance: {distance}, Radius: {radius}')