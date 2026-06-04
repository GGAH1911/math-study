import numpy as np
from sympy import sqrt, Rational, simplify

# 주어진 조건 검증
A = np.array([0, 0])
B = np.array([-3/2, 3*np.sqrt(3)/2])
C = np.array([5, 0])
P = np.array([3, 0])
Q = np.array([141/49, 24*np.sqrt(3)/49])

# 변의 길이 검증
AB = np.linalg.norm(B - A)
AC = np.linalg.norm(C - A)
BC = np.linalg.norm(C - B)
AP = np.linalg.norm(P - A)
AQ = np.linalg.norm(Q - A)
PB = np.linalg.norm(B - P)

# 조건 확인
assert abs(AB - 3) < 1e-10, f'AB = {AB}'
assert abs(AC - 5) < 1e-10, f'AC = {AC}'
assert abs(BC - 7) < 1e-10, f'BC = {BC}'
assert abs(AP - 3) < 1e-10, f'AP = {AP}'
assert abs(AQ - 3) < 1e-10, f'AQ = {AQ}'
assert abs(PB - 3*np.sqrt(3)) < 1e-10, f'PB = {PB}'

# cos A 확인
cos_A = np.dot(B, C) / (AB * AC)
assert abs(cos_A - (-0.5)) < 1e-10, f'cos A = {cos_A}'

# P가 AC 위에 있는지 확인 (P = λC for 0 < λ < 1)
assert abs(P[1]) < 1e-10 and 0 < P[0] < 5, 'P not on AC'

# Q가 BC 위에 있는지 확인
t = np.linalg.norm(Q - B) / np.linalg.norm(C - B)
assert 0 <= t <= 1, f't = {t}'

# PQ 길이
PQ = np.linalg.norm(Q - P)
expected = 6/7
assert abs(PQ - expected) < 1e-10, f'PQ = {PQ}'

print('VERIFY_PASS')