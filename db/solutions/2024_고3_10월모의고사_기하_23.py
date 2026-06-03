import sympy as sp
from sympy import sqrt, symbols

# 쌍곡선: x^2/2 - y^2 = 1
a_sq = 2
b_sq = 1

# 초점의 관계식: c^2 = a^2 + b^2
c_sq = a_sq + b_sq
c = sqrt(c_sq)

# 두 초점 사이의 거리
distance = 2 * c

# 답: 2√3
expected = 2 * sqrt(3)

# 검증: 쌍곡선 위의 점에서 초점 성질 확인
# 꼭짓점 (√2, 0)에서 두 초점까지 거리 차이가 2a인지 확인
vertex_x = sqrt(a_sq)
focus_left = -sqrt(c_sq)
focus_right = sqrt(c_sq)

dist_to_left = abs(vertex_x - focus_left)
dist_to_right = abs(vertex_x - focus_right)
diff = dist_to_left - dist_to_right

if distance == expected and abs(diff - 2*sqrt(a_sq)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')