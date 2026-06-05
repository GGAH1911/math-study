import sympy as sp
import numpy as np

# 설정: A의 좌표 (원점에서 거리 7)
# a^2 + b^2 + c^2 = 49
# xy평면과의 교선원 반지름이 5 → c^2 = 39
c_squared = 39
ab_squared = 49 - 39
print(f'a^2 + b^2 = {ab_squared}')

# 구의 중심에서 z축까지 거리: sqrt(a^2 + b^2)
dist_to_z_axis_sq = ab_squared

# z축과의 교점: (z-c)^2 = 64 - (a^2 + b^2) = 64 - 10 = 54
z_diff_sq = 64 - dist_to_z_axis_sq
print(f'(z-c)^2 = {z_diff_sq}')

z_diff = np.sqrt(z_diff_sq)
print(f'z - c = ±{z_diff}')
print(f'z - c = ±3√6, and 3√6 ≈ {3*np.sqrt(6)}')

# BC 길이
BC_length = 2 * z_diff
expected = 6 * np.sqrt(6)
print(f'BC = {BC_length}')
print(f'6√6 ≈ {expected}')

if np.isclose(BC_length, expected):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')