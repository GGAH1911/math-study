# 무게중심 검증
import numpy as np

# 구한 A의 좌표
A = np.array([-2, -4])

# B와 C는 중점이 (1, 2)이고 B + C = (2, 4)를 만족하는 임의의 두 점
# 예: B = (0, 1), C = (2, 3) (중점 = (1, 2))
B = np.array([0, 1])
C = np.array([2, 3])

# 무게중심 검증
centroid = (A + B + C) / 3
print(f'Centroid: {centroid}')
assert np.allclose(centroid, [0, 0]), 'Centroid should be at origin'

# BC 중점 검증
midpoint_BC = (B + C) / 2
print(f'Midpoint of BC: {midpoint_BC}')
assert np.allclose(midpoint_BC, [1, 2]), 'Midpoint of BC should be (1, 2)'

# 답 검증
answer = (-2) * (-4)
print(f'a × b = {answer}')
assert answer == 8, f'Expected 8, got {answer}'

print('VERIFY_PASS')