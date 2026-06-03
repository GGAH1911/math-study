import numpy as np

r = 4
circle_area = np.pi * r**2  # 16π

# 활꼴 BC: 중심각 45° = π/4
theta_BC = np.pi / 4
sector_BC = 0.5 * r**2 * theta_BC
triangle_BC = 0.5 * r**2 * np.sin(theta_BC)
segment_BC = sector_BC - triangle_BC

# 활꼴 DEF: 중심각 90° = π/2
theta_DEF = np.pi / 2
sector_DEF = 0.5 * r**2 * theta_DEF
triangle_DEF = 0.5 * r**2 * np.sin(theta_DEF)
segment_DEF = sector_DEF - triangle_DEF

# 활꼴 GH: 중심각 45° = π/4
segment_GH = segment_BC

# Step I: 원 - 3개의 활꼴
area_I = circle_area - segment_BC - segment_DEF - segment_GH

# Step II: y축 대칭 접기 (절반)
area_II = area_I / 2

# Step III: 2장 붙이기
area_III = 2 * area_II  # == area_I

# 기댓값: 8 + 8π + 8√2
expected = 8 + 8 * np.pi + 8 * np.sqrt(2)

if abs(area_III - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Computed: {area_III:.10f}')
    print(f'Expected: {expected:.10f}')
