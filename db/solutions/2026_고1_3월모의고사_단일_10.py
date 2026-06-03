import numpy as np

# 산점도의 15개 점
points = [
    (6, 9), (8, 7), (8, 5), (8, 3),
    (10, 6), (10, 5), (10, 4),
    (12, 8), (12, 5), (12, 3),
    (14, 1), (15, 5), (15, 3),
    (18, 2), (20, 2)
]

# 운동 시간들
motion_times = [y for x, y in points]

# 최빈값 계산
from collections import Counter
freq = Counter(motion_times)
mode = max(freq, key=freq.get)
a = mode

# x >= 15인 점들
ge15_points = [p for p in points if p[0] >= 15]
ge15_motion_times = [y for x, y in ge15_points]
b = np.mean(ge15_motion_times)

result = a + b

if abs(result - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')