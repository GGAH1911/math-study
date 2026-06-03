import numpy as np

# 정육각형 ABCDEF, 한 변의 길이 = 1, 중심 원점
# 꼭짓점 각도: A=120°, B=180°, C=240°, D=300°, E=0°, F=60°
angles_deg = [120, 180, 240, 300, 0, 60]
angles_rad = [a * np.pi / 180 for a in angles_deg]

A, B, C, D, E, F = [np.array([np.cos(r), np.sin(r)]) for r in angles_rad]

# 변 길이 검증
side = np.linalg.norm(B - A)
assert abs(side - 1.0) < 1e-9, f'Side length error: {side}'

# 벡터 계산
AE = E - A  # (3/2, -√3/2)
BC = C - B  # (1/2, -√3/2)

result = AE + BC  # (2, -√3)
magnitude = np.linalg.norm(result)

expected = np.sqrt(7)

if abs(magnitude - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {magnitude}, expected {expected}')
