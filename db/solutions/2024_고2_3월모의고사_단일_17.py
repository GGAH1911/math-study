import sympy as sp
from sympy import sqrt, simplify

# 주어진 조건 검증
a = sqrt(5) - 1
k = 4

# 조건 (가): 직선 PQ의 기울기 = -1
slope = (k/(a+2) - k/a) / 2
slope_simplified = simplify(slope)
assert slope_simplified == -1, f'기울기 조건 실패: {slope_simplified}'

# 조건 (나): 사각형 PQRS의 넓이 = 8√5
area = 8 * (a + 1)
area_simplified = simplify(area)
expected_area = 8 * sqrt(5)
assert simplify(area_simplified - expected_area) == 0, f'넓이 조건 실패: {area_simplified}'

print('VERIFY_PASS')