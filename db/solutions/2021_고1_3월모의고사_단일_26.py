import numpy as np

# 검증: 구체적 예시로 확인
# A = (0, 0), B = (8, 0), C = (4, 32)
A = np.array([0, 0])
B = np.array([8, 0])
C = np.array([4, 32])

# 점들의 위치
D = A + (1/4) * (B - A)  # (2, 0)
E = A + (1/2) * (B - A)  # (4, 0)
F = A + (1/4) * (C - A)  # (1, 8)
G = A + (1/2) * (C - A)  # (2, 16)

# 조건 검증
AD = np.linalg.norm(D - A)
DE = np.linalg.norm(E - D)
AE = np.linalg.norm(E - A)
EB = np.linalg.norm(B - E)
AF = np.linalg.norm(F - A)
FG = np.linalg.norm(G - F)
AG = np.linalg.norm(G - A)
GC = np.linalg.norm(C - G)

assert np.isclose(AD, DE), f'AD={AD}, DE={DE}'
assert np.isclose(AE, EB), f'AE={AE}, EB={EB}'
assert np.isclose(AF, FG), f'AF={AF}, FG={FG}'
assert np.isclose(AG, GC), f'AG={AG}, GC={GC}'

# 신발끈 공식으로 사각형 DFGE 넓이
def shoelace(p1, p2, p3, p4):
    return 0.5 * abs((p1[0]*(p2[1]-p4[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p4[1]-p2[1]) + p4[0]*(p1[1]-p3[1])))

area_dfge = shoelace(D, F, G, E)
assert np.isclose(area_dfge, 24), f'DFGE area={area_dfge}'

# 삼각형 ABC 넓이
area_abc = 0.5 * abs(np.cross(B - A, C - A))
assert np.isclose(area_abc, 128), f'ABC area={area_abc}'

print('VERIFY_PASS')