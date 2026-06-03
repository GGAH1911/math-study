import numpy as np

# 확정 값
k, a = 4, 2

# 점 좌표
A = np.array([k, 2**(k-1) + 1])          # (4, 9)
B = np.array([k, np.log2(k - a)])          # (4, 1)
C_x = k - 2
C_y = 2**(C_x - 1) + 1                    # C on exp curve
C = np.array([C_x, C_y])                   # (2, 3)
# D: log2(x-a)=0 -> x-a=1 -> x=a+1
D = np.array([a + 1, 0])                   # (3, 0)

# 조건 검증
AB = np.linalg.norm(A - B)
BC = np.linalg.norm(B - C)

# BC 직선 기울기 확인
slope_BC = (C[1] - B[1]) / (C[0] - B[0]) if C[0] != B[0] else float('inf')

# C가 y=2^{x-1}+1 위에 있는지
C_on_curve = abs(C[1] - (2**(C[0]-1) + 1)) < 1e-9

# 사각형 ACDB 넓이 (신발끈)
verts = [A, C, D, B]
n = len(verts)
area = 0.0
for i in range(n):
    j = (i + 1) % n
    area += verts[i][0] * verts[j][1]
    area -= verts[j][0] * verts[i][1]
area = abs(area) / 2

ok = (
    abs(AB - 8) < 1e-9 and
    abs(BC - 2*np.sqrt(2)) < 1e-9 and
    abs(slope_BC - (-1)) < 1e-9 and
    C_on_curve and
    0 < a < k and
    abs(area - 10) < 1e-9
)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
