import sympy as sp
from sympy import pi, sqrt, simplify, integrate, Rational

# 좌표계 설정
A1 = (0, 0)
B1 = (4, 0)
center = (2, 0)
radius = 2

# 반원의 호를 4등분한 점들 (A1에서 가까운 순서)
# A1(180°) -> C1(135°) -> D1(90°) -> E1(45°) -> B1(0°)
C1 = (2 - sqrt(2), sqrt(2))
D1 = (2, 2)
E1 = (2 + sqrt(2), sqrt(2))

# C1, E1에서 A1B1에 내린 수선의 발
A2 = (2 - sqrt(2), 0)
B2 = (2 + sqrt(2), 0)

# 직사각형 C1A2B2E1의 넓이
rect_area = simplify((B2[0] - A2[0]) * (C1[1] - 0))

# 삼각형 A1D1B1의 넓이
tri_area = Rational(1, 2) * 4 * 2

# 직사각형과 삼각형의 교집합 넓이 (적분으로 계산)
x = sp.symbols('x')

# 구간 1: [2-sqrt(2), sqrt(2)]에서 y ∈ [0, x]
int1 = integrate(x, (x, 2 - sqrt(2), sqrt(2)))

# 구간 2: [sqrt(2), 4-sqrt(2)]에서 y ∈ [0, sqrt(2)]
int2 = integrate(sqrt(2), (x, sqrt(2), 4 - sqrt(2)))

# 구간 3: [4-sqrt(2), 2+sqrt(2)]에서 y ∈ [0, -x+4]
int3 = integrate(-x + 4, (x, 4 - sqrt(2), 2 + sqrt(2)))

intersection_area = simplify(int1 + int2 + int3)

# 직사각형과 삼각형의 합집합 넓이
union_area = simplify(rect_area + tri_area - intersection_area)

# 반원의 넓이
semicircle_area = pi * radius**2 / 2

# 첫 번째 색칠 영역의 넓이
S1 = simplify(semicircle_area - union_area)

# 다음 반원의 지름
next_diameter = B2[0] - A2[0]
next_diameter = simplify(next_diameter)

# 넓이 비율 계산
length_ratio = simplify(next_diameter / 4)
area_ratio = simplify(length_ratio**2)

# 무한급수의 합
# S_n = S1 * (area_ratio)^(n-1)
# lim sum(S_n) = S1 / (1 - area_ratio)
infinite_sum = simplify(S1 / (1 - area_ratio))

# 예상 답
expected_answer = 4*pi + 16*sqrt(2) - 32

# 검증
difference = simplify(infinite_sum - expected_answer)
if difference == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")