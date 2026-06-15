import numpy as np
from scipy.optimize import fmin

CANDIDATE = 60

# 최적점에서의 벡터들
OA = np.array([1, 0, 0])
OB = np.array([-4/5, -3/5, 0])
OC = np.array([0, 1, 0])

# 조건 검증
x = 4
cond_vector = x * OA + 5 * OB + 3 * OC
cond_zero = np.allclose(cond_vector, 0)

# 원 위의 점 검증
radius_check = np.allclose([np.linalg.norm(OA), np.linalg.norm(OB), np.linalg.norm(OC)], 1)

# 세 점이 다른지 확인
points_different = (not np.allclose(OA, OB)) and (not np.allclose(OB, OC)) and (not np.allclose(OC, OA))

# 넓이 계산
AB = OB - OA
AC = OC - OA
cross_product = np.cross(AB, AC)
area = 0.5 * np.linalg.norm(cross_product)

# 최적성 검증: 내적 최대화 조건
p = np.dot(OA, OB)
q = np.dot(OB, OC)
expected_p = (-5 - 3*q) / x
p_correct = np.isclose(p, expected_p)

result = 50 * area

if (cond_zero and radius_check and points_different and p_correct and 
    np.isclose(result, CANDIDATE)):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')