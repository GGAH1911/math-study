import math
from math import sqrt

# 주어진 조건
A = (2, 2, -1)
C = (-2, 1, 1)

# A를 x축에 대하여 대칭이동
B = (A[0], -A[1], -A[2])
B = (2, -2, 1)

# BC의 길이 계산
dist_BC = sqrt((B[0] - C[0])**2 + (B[1] - C[1])**2 + (B[2] - C[2])**2)

print(f'B = {B}')
print(f'C = {C}')
print(f'|BC| = {dist_BC}')

if abs(dist_BC - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')