import numpy as np
from scipy.optimize import fsolve

# 원의 중심과 반지름
h, k = 3, 0
r = 5

# 점들의 좌표
A = np.array([-2, 0])
B = np.array([8, 0])
C = np.array([0, -4])
D = np.array([0, 4])

# 조건 (가) 확인: AB를 1:4로 내분하는 점 = CD의 중점
P = A + (1/5) * (B - A)
M = (C + D) / 2
assert np.allclose(P, M), f"P={P}, M={M}"

# 조건 (나) 확인: 원이 직선 4x - 3y + 13 = 0에 접함
center = np.array([h, k])
dist = abs(4*h - 3*k + 13) / np.sqrt(16 + 9)
assert np.isclose(dist, r), f"distance={dist}, r={r}"

# 원 위의 점들 확인
assert np.isclose((A[0]-h)**2 + (A[1]-k)**2, r**2)
assert np.isclose((B[0]-h)**2 + (B[1]-k)**2, r**2)
assert np.isclose((C[0]-h)**2 + (C[1]-k)**2, r**2)
assert np.isclose((D[0]-h)**2 + (D[1]-k)**2, r**2)

# Shoelace 공식으로 넓이 계산
verts = np.array([A, C, B, D])
area = 0.5 * abs(sum(verts[i][0]*verts[(i+1)%4][1] - verts[(i+1)%4][0]*verts[i][1] for i in range(4)))
assert area == 40, f"area={area}"

print('VERIFY_PASS')