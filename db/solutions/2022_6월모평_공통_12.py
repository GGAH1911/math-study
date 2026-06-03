import numpy as np

# 주어진 조건
AB = 4
AC = 5
cos_BAC = 1/8

# BC 계산
BC2 = AB**2 + AC**2 - 2*AB*AC*cos_BAC
BC = BC2**0.5
assert abs(BC - 6) < 1e-9

# 좌표 설정
B = np.array([0.0, 0.0])
C = np.array([6.0, 0.0])
# A 좌표
ax = (AB**2 - AC**2 + BC**2) / (2*BC)  # = 9/4
ay = (AB**2 - ax**2)**0.5              # = 5√7/4
A = np.array([ax, ay])

# AB, AC 검증
assert abs(np.linalg.norm(A-B) - 4) < 1e-9
assert abs(np.linalg.norm(A-C) - 5) < 1e-9

# cos(∠BAC) 검증
vAB = B - A; vAC = C - A
cos_check = np.dot(vAB, vAC) / (np.linalg.norm(vAB)*np.linalg.norm(vAC))
assert abs(cos_check - 1/8) < 1e-9

# D: AD=1, D on AC
D = A + (1/5)*(C - A)  # AD = AC/5 = 1
assert abs(np.linalg.norm(D-A) - 1) < 1e-9
assert abs(np.linalg.norm(D-B) - 4) < 1e-9  # BD=4

# E 좌표
E = np.array([10/3, 0.0])

# ∠BED 검증
vEB = B - E; vED = D - E
cos_BED = np.dot(vEB, vED) / (np.linalg.norm(vEB)*np.linalg.norm(vED))
assert abs(cos_BED - 1/8) < 1e-9

# ∠BDA 검증
vDB = B - D; vDA = A - D
cos_BDA = np.dot(vDB, vDA) / (np.linalg.norm(vDB)*np.linalg.norm(vDA))
assert abs(cos_BDA - 1/8) < 1e-9

# DE 계산
DE = np.linalg.norm(D - E)
assert abs(DE - 8/3) < 1e-9

print('VERIFY_PASS')
