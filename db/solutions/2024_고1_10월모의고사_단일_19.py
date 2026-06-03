import sympy as sp
from sympy import sqrt, Rational

a = Rational(3, 2)
b = Rational(11, 2)

# A, B의 좌표
A_x, A_y = a, -a**2 + 6*a
B_x, B_y = b, -b**2 + 6*b

# 원의 중심 (AB의 중점)
O_x = (a + b) / 2
O_y = (A_y + B_y) / 2

# 원의 반지름 (AB를 지름으로)
radius = sqrt((B_x - A_x)**2 + (B_y - A_y)**2) / 2

# 조건 1: 원의 넓이 = 8π
area = sp.pi * radius**2
check1 = (area - 8*sp.pi == 0)

# 조건 2: 점 A를 지나고 기울기 1인 직선이 원에 접함
# 직선: x - y + (5a - a²) = 0
line_c = 5*a - a**2
distance = abs(O_x - O_y + line_c) / sqrt(2)
check2 = (distance - radius == 0) or (distance + radius == 0)

# 답: y절편
y_intercept = a * b

print(f"A: ({A_x}, {A_y})")
print(f"B: ({B_x}, {B_y})")
print(f"원의 중심 O: ({O_x}, {O_y})")
print(f"원의 반지름: {radius}")
print(f"넓이 조건 확인: {sp.simplify(area - 8*sp.pi) == 0}")
print(f"접선 거리: {distance}")
print(f"접선 조건 확인: {sp.simplify(distance - radius) == 0}")
print(f"y절편: {y_intercept}")

if check1 and check2:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")