import sympy as sp
from sympy import sqrt, cos, sin, pi, simplify

CANDIDATE = 20

# 좌표 설정
O = sp.Matrix([0, 0])
A = sp.Matrix([2, 0])
B = sp.Matrix([0, 2])

# 점 P 좌표: θ = 5π/6
theta = 5*pi/6
P = sp.Matrix([2*cos(theta), 2*sin(theta)])
P_simplified = sp.Matrix([-sqrt(3), 1])

# 각도 검증: ∠BAP = π/6
AB = B - A
AP = P - A

cos_angle = (AB.dot(AP)) / (AB.norm() * AP.norm())
cos_angle_simplified = simplify(cos_angle)
expected_cos = sqrt(3)/2

# 수선의 발 H 계산
s = ((B - A).dot(AP)) / AP.dot(AP)
s_simplified = simplify(s)

H = A + s_simplified * AP
H_simplified = sp.simplify(H)

# OH² 계산
OH_squared = H_simplified.dot(H_simplified)
OH_squared_simplified = simplify(OH_squared)

# m + n√3 형태로 표현
# OH² = 4 - 2√3이므로 m = 4, n = -2
m = 4
n = -2
answer = m**2 + n**2

# 검증
if simplify(OH_squared_simplified - (m + n*sqrt(3))) == 0 and answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: OH²={OH_squared_simplified}, m²+n²={answer}")