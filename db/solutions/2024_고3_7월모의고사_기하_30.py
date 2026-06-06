import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
A = np.array([0, 0, 9])
A_prime = np.array([0, 0, 0])
P = np.array([5, 0, 0])
B_prime = np.array([-7/5, 24/5, 0])
M = np.array([9/5, 12/5, 0])
B = np.array([-7/5, 24/5, 10])

# 조건 검증
AA_prime = np.linalg.norm(A - A_prime)
A_prime_P = np.linalg.norm(P - A_prime)
A_prime_B_prime = np.linalg.norm(B_prime - A_prime)
PB_prime = np.linalg.norm(B_prime - P)

assert abs(AA_prime - 9) < 1e-10
assert abs(A_prime_P - 5) < 1e-10
assert abs(A_prime_B_prime - 5) < 1e-10
assert abs(PB_prime - 8) < 1e-10

# M이 PB'의 중점인지 확인
M_check = (P + B_prime) / 2
assert np.allclose(M, M_check)

# 각 MAB = π/2 확인
vec_AM = M - A
vec_AB = B - A
dot_product = np.dot(vec_AM, vec_AB)
assert abs(dot_product) < 1e-10

# 평면 APB'의 법선벡터
vec_AP = P - A
vec_AB_prime = B_prime - A
normal = np.cross(vec_AP, vec_AB_prime)
normal = normal / np.gcd.reduce(normal.astype(int))

# 직선 BM의 방향벡터
vec_BM = M - B

# 직선과 평면이 이루는 각
sin_theta = abs(np.dot(vec_BM, normal)) / (np.linalg.norm(vec_BM) * np.linalg.norm(normal))
cos_squared_theta = 1 - sin_theta**2

# 분수로 표현
from fractions import Fraction
cos_squared_frac = Fraction(53, 58)

assert abs(cos_squared_theta - float(cos_squared_frac)) < 1e-10

print('VERIFY_PASS')