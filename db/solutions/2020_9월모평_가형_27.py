import math
from sympy import symbols, solve, simplify

CANDIDATE = 90

# 포물선 y^2 = 4x 위의 점 A(a, y_a), B(b, y_b)
# 초점 F(1, 0), 준선 x = -1
# 포물선 성질: 초점까리의 거리 = 준선까지의 거리
# AF = a + 1, BF = b + 1

# 무게중심 x좌표: (a + b + 1)/3 = 6
# a + b = 17

# 서로 다른 두 점이므로 a ≠ b
# x좌표는 1보다 큰 자연수이므로 a, b ≥ 2

a_plus_b = 17
max_product = 0
best_a, best_b = None, None

for a in range(2, 16):  # a < 17이고 a ≥ 2
    b = a_plus_b - a
    if b >= 2 and a != b:
        product = (a + 1) * (b + 1)
        if product > max_product:
            max_product = product
            best_a, best_b = a, b

# 검증
print(f"최적: a={best_a}, b={best_b}")
print(f"a + b = {best_a + best_b} (should be 17)")
print(f"무게중심 x좌표: {(best_a + best_b + 1)/3} (should be 6)")
print(f"AF × BF = ({best_a}+1) × ({best_b}+1) = {best_a + 1} × {best_b + 1} = {(best_a + 1) * (best_b + 1)}")
print(f"CANDIDATE = {CANDIDATE}")

if max_product == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {max_product}, got {CANDIDATE}")