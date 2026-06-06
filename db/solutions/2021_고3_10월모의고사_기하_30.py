import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
A = np.array([2, 2*np.sqrt(3), 0])
B = np.array([0, 0, 0])
C = np.array([4, 0, 0])
D = np.array([2, 2*np.sqrt(3), 2])
E = np.array([2, 0, 0])

# H 계산
H = np.array([2, 3*np.sqrt(3)/2, 3/2])

# 조건 (나) 검증
DE_dist = np.linalg.norm(D - E)
assert abs(DE_dist - 4) < 1e-9, f"DE = {DE_dist}, should be 4"

# ∠CED = 90° 검증
EC = C - E
ED = D - E
assert abs(np.dot(EC, ED)) < 1e-9, "EC ⊥ ED should hold"

# H가 평면 BCD 위에 있는지 확인
BC = C - B
BD = D - B
normal = np.cross(BC, BD)
assert abs(np.dot(normal, H - B)) < 1e-9, "H should be on plane BCD"

# AH가 평면 BCD의 법선 방향인지 확인
AH = H - A
normal_unit = normal / np.linalg.norm(normal)
assert abs(abs(np.dot(AH, normal_unit)) - np.linalg.norm(AH)) < 1e-9, "AH should be perpendicular to plane BCD"

# 조건 (가) 검증
EA = A - E
EH = H - E
cos_AEH = np.dot(EA, EH) / (np.linalg.norm(EA) * np.linalg.norm(EH))

AD = D - A
cos_DAH = np.dot(AD, AH) / (np.linalg.norm(AD) * np.linalg.norm(AH))

assert abs(cos_AEH - cos_DAH) < 1e-9, f"∠AEH ≠ ∠DAH: {cos_AEH} vs {cos_DAH}"

# 정사영 넓이 계산
AH_cross_AD = np.cross(AH, AD)
triangle_area = 0.5 * np.linalg.norm(AH_cross_AD)

AB = B - A
ABD_normal = np.cross(AB, AD)
cos_theta = abs(np.dot(AH_cross_AD, ABD_normal)) / (np.linalg.norm(AH_cross_AD) * np.linalg.norm(ABD_normal))

projection_area = triangle_area * cos_theta

# 답 검증: 정사영 넓이 = 3/4
assert abs(projection_area - 0.75) < 1e-9, f"Projection area = {projection_area}, should be 0.75"

print("VERIFY_PASS")