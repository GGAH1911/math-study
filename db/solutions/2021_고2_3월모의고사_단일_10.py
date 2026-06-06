import sympy as sp
from sympy import sqrt, simplify

# 원의 중심
center_x, center_y = 1, 0

# 직선: x + 2y + 5 = 0
# 점 (center_x, center_y)에서 직선 ax + by + c = 0까지의 거리
a, b, c = 1, 2, 5
r_candidate = abs(a*center_x + b*center_y + c) / sqrt(a**2 + b**2)
r_candidate = simplify(r_candidate)

# 검증: r = 6√5/5인지 확인
r_answer = 6*sqrt(5)/5

# 거리가 r과 같은지 확인
if simplify(r_candidate - r_answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')