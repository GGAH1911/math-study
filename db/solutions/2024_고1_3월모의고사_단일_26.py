import math
from math import sqrt

# 정사각형 꼭짓점
A = (0, 4*sqrt(2))
B = (0, 0)
C = (4*sqrt(2), 0)
D = (4*sqrt(2), 4*sqrt(2))

# 점 E: AD 위에서 DE = sqrt(2)/2
E = (4*sqrt(2) - sqrt(2)/2, 4*sqrt(2))
E = (7*sqrt(2)/2, 4*sqrt(2))

# EC 거리 계산
EC = sqrt((C[0] - E[0])**2 + (C[1] - E[1])**2)
print(f'EC = {EC} (expected {sqrt(130)/2})')

# k 계산
k = EC / sqrt(65)
print(f'k = {k} (expected {sqrt(2)/2})')

# EF, FC 거리
EF = 4 * k
FC = 7 * k
print(f'EF = {EF} (expected {2*sqrt(2)})')
print(f'FC = {FC} (expected {7*sqrt(2)/2})')

# 둘레 계산
AE = sqrt((E[0] - A[0])**2 + (E[1] - A[1])**2)
AB = 4*sqrt(2)
BC = 4*sqrt(2)

perimeter = AB + BC + FC + EF + AE
print(f'\nPerimeter a = {perimeter} (expected {17*sqrt(2)})')
print(f'a^2 = {perimeter**2} (expected 578)')

if abs(perimeter**2 - 578) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')