import numpy as np

# 세 점 A, B, C를 설정
# 임의로 좌표 설정 (일직선상에 있지 않도록)
A = np.array([0.0, 0.0])
B = np.array([1.0, 0.0])
C = np.array([0.0, 1.0])

# 벡터 계산
vec_AB = B - A
vec_BC = C - B
vec_CA = A - C

# p=2, q=-2에 대해 검증
p = 2
q = -2

# 좌변 계산: 2*AB + p*BC
left_side = 2 * vec_AB + p * vec_BC

# 우변 계산: q*CA
right_side = q * vec_CA

# 검증: 좌변과 우변이 같은지 확인
if np.allclose(left_side, right_side):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')