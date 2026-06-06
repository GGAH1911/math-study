import math
from sympy import sqrt, simplify, solve

# 주어진 조건
r = 4*sqrt(3)/3  # 내접원의 반지름
BD = 12
DC = 4
BC = BD + DC  # BC = 16

# 구한 답
x = 2
AB = x + 12  # AB = 14
AC = x + 4   # AC = 6

# 검증: 헤론의 공식으로 넓이 계산
s = (BC + AB + AC) / 2  # 반둘레
area_heron = math.sqrt(s * (s - BC) * (s - AB) * (s - AC))

# 내접원 공식으로 반지름 계산
r_calculated = area_heron / s
r_expected = float(4*sqrt(3)/3)

# 검증
if abs(r_calculated - r_expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')