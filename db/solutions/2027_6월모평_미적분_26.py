import numpy as np

# 원래 함수: y = sin(x), 0 < x < pi
# 직선 y = sqrt(3)/2 와의 교점
target_y = np.sqrt(3) / 2

# 교점 x 좌표
xA = np.pi / 3
xB = 2 * np.pi / 3

# 교점이 실제로 y = sqrt(3)/2 위에 있는지 확인
assert abs(np.sin(xA) - target_y) < 1e-10, 'A is not on curve'
assert abs(np.sin(xB) - target_y) < 1e-10, 'B is not on curve'

# 접선 기울기
mA = np.cos(xA)  # = 1/2
mB = np.cos(xB)  # = -1/2

# 두 직선이 이루는 예각의 tan
tan_theta = abs((mA - mB) / (1 + mA * mB))

# 정답: 4/3
expected = 4 / 3

if abs(tan_theta - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', tan_theta, expected)
