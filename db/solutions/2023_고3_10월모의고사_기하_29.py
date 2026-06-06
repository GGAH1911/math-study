import math
from decimal import Decimal

# 점 P 계산
p_x = 4/5
p_y = 2*math.sqrt(21)/5

# 점 Q 계산
q_x = 24/5
q_y = 2*math.sqrt(6)/5

# 조건 검증
assert abs(p_x**2 + p_y**2 - 4) < 1e-10, 'P condition 1 failed'
assert abs(p_x*(p_x-5) + p_y**2) < 1e-10, 'P condition 2 failed'
assert abs((q_x-5)**2 + q_y**2 - 1) < 1e-10, 'Q condition 1 failed'
assert abs(q_x*(q_x-5) + q_y**2) < 1e-10, 'Q condition 2 failed'

# OA · PQ 계산
OA = (5, 0)
PQ = (q_x - p_x, q_y - p_y)
result = OA[0]*PQ[0] + OA[1]*PQ[1]

if abs(result - 20) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')