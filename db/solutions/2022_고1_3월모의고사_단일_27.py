import numpy as np
from sympy import *

# 점들의 정확한 좌표
P = [Rational(3,2), sqrt(3)/2]
H = [sqrt(3), 0]
Q = [sqrt(3), 1]

# 벡터
vec_PH = [H[0] - P[0], H[1] - P[1]]
vec_PQ = [Q[0] - P[0], Q[1] - P[1]]

# 외적으로 넓이 계산
cross = vec_PH[0] * vec_PQ[1] - vec_PH[1] * vec_PQ[0]
area = abs(cross) / 2

# 기댓값
expected_area = (2*sqrt(3) - 3) / 4

# 검증
if simplify(area - expected_area) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')