import math
from sympy import *

# 조건 설정
r = sqrt(3)/2
sqrt3 = sqrt(3)

# 원 O
O = (0, 0)
A = (-sqrt3/2, 0)
B = (sqrt3/2, 0)
C = (0, sqrt3/2)

# 원 O'
O_prime = (0, 1 + sqrt3)
r_prime_sq = (sqrt3/2)**2 + (1 + sqrt3)**2
r_prime_sq_simplified = nsimplify(r_prime_sq)
r_prime = sqrt(r_prime_sq_simplified)

# 검증: 공통현 확인
dist_OA = sqrt((A[0]-O[0])**2 + (A[1]-O[1])**2)
dist_OB = sqrt((B[0]-O[0])**2 + (B[1]-O[1])**2)

# 원 O' 위의 점인지 확인
dist_O_prime_A = sqrt((A[0]-O_prime[0])**2 + (A[1]-O_prime[1])**2)
dist_O_prime_B = sqrt((B[0]-O_prime[0])**2 + (B[1]-O_prime[1])**2)

# ∠ACB 확인
CA = (A[0]-C[0], A[1]-C[1])
CB = (B[0]-C[0], B[1]-C[1])
dot_product = CA[0]*CB[0] + CA[1]*CB[1]

# C, O, O'이 일직선인지 확인 (모두 x = 0인지)
collinear = (C[0] == 0 and O[0] == 0 and O_prime[0] == 0)

# 최종 검증
if (nsimplify(dist_OA - r) == 0 and 
    nsimplify(dist_O_prime_A - r_prime) == 0 and
    nsimplify(dot_product) == 0 and
    collinear):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')