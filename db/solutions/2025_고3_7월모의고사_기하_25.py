import sympy as sp
from sympy import sqrt, symbols

x, y = symbols('x y', real=True)

# 주어진 점들
O = (0, 0)
A = (3, 4)
B = (-3, 6)

# P는 직선 x - 2y + 5 = 0 위의 점
# P = (2y - 5, y)로 매개변수화
t = symbols('t', real=True)
P = (2*t - 5, t)

# 벡터들
OP = (P[0] - O[0], P[1] - O[1])
OA = (A[0] - O[0], A[1] - O[1])
OB = (B[0] - O[0], B[1] - O[1])

# 조건 확인
OP_minus_OA = (OP[0] - OA[0], OP[1] - OA[1])
dot_product = OP_minus_OA[0] * OB[0] + OP_minus_OA[1] * OB[1]
dot_product_simplified = sp.simplify(dot_product)
print(f"Dot product simplified: {dot_product_simplified}")

# |OP|의 제곱
OP_magnitude_squared = OP[0]**2 + OP[1]**2
OP_magnitude_squared = sp.expand(OP_magnitude_squared)
print(f"|OP|^2 = {OP_magnitude_squared}")

# 최솟값을 구하기 위해 미분
derivative = sp.diff(OP_magnitude_squared, t)
print(f"d(|OP|^2)/dt = {derivative}")

# 최솟값을 주는 t
t_min = sp.solve(derivative, t)[0]
print(f"t at minimum: {t_min}")

# 최솟값
OP_magnitude_squared_min = OP_magnitude_squared.subs(t, t_min)
print(f"|OP|^2 at minimum: {OP_magnitude_squared_min}")

OP_magnitude_min = sp.sqrt(OP_magnitude_squared_min)
print(f"|OP| at minimum: {OP_magnitude_min}")

# 검증: 이것이 sqrt(5)인지 확인
if OP_magnitude_min == sqrt(5):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")