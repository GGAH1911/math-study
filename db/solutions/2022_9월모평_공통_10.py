import numpy as np

a = 5/2
b = 1/2

# 두 교점 좌표
x_A = 1 / (2*b)
x_B = 5 / (2*b)
y_A = a * np.sin(b * np.pi * x_A)
y_B = a * np.sin(b * np.pi * x_B)

# 1) A, B 가 y=a 위에 있는지
assert abs(y_A - a) < 1e-9, f'y_A={y_A} != a={a}'
assert abs(y_B - a) < 1e-9, f'y_B={y_B} != a={a}'

# 2) 삼각형 OAB 넓이 = 5
base = x_B - x_A
height = a  # y=a 까지의 수직 거리 (O는 원점)
area = 0.5 * base * height
assert abs(area - 5) < 1e-9, f'area={area}'

# 3) 기울기 곱 = 5/4
slope_OA = y_A / x_A
slope_OB = y_B / x_B
product = slope_OA * slope_OB
assert abs(product - 5/4) < 1e-9, f'product={product}'

# 4) 정의역 내 존재 확인
assert 0 <= x_A <= 3/b and 0 <= x_B <= 3/b, 'out of domain'

print('VERIFY_PASS')
