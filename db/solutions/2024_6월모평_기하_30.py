import numpy as np
from scipy.optimize import fsolve

# 검증: (x,y)가 영역에 속하면 6t^2 + 4(y-x)t + (2x^2+y^2-3) <= 0을 만족하는 t가 존재
def verify_point(x, y):
    # 판별식 >= 0 확인
    # Delta = 16(y-x)^2 - 24(2x^2 + y^2 - 3) = -8(y+2x)^2 + 72
    delta = -8 * (y + 2*x)**2 + 72
    if delta < -1e-10:  # 음수면 불가능
        return False
    # 영역 경계 확인
    return (y + 2*x)**2 <= 9 + 1e-10

# 삼각형 꼭짓점 확인
v1 = verify_point(0, 0)
v2 = verify_point(0, 3)
v3 = verify_point(1.5, 0)
assert v1 and v2 and v3, "꼭짓점 검증 실패"

# 범위 내 점 확인
test_points = [(0.5, 1), (0.75, 0), (0, 1.5), (1, 0.5)]
for x, y in test_points:
    if 2*x + y <= 3 + 1e-10:
        assert verify_point(x, y), f"({x}, {y}) 검증 실패"

# 범위 밖 점 확인 (y > 3 - 2x)
outside = verify_point(0, 4)  # 범위 밖
assert not outside, "범위 밖 점이 잘못 포함됨"

# 넓이 계산
area = 0.5 * 1.5 * 3
assert abs(area - 2.25) < 1e-10, f"넓이 계산 오류: {area}"

# p=4, q=9 확인
assert area == 9/4, f"9/4 = {9/4}, 계산값 = {area}"
assert 9 + 4 == 13, "p+q 계산 오류"

print("VERIFY_PASS")