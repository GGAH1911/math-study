import numpy as np

# 도로망 구조를 반영한 경로의 수 계산
f = np.zeros((5, 4), dtype=int)
f[0, 0] = 1

# 행 0 (P행): (0,0)부터 (3,0)까지만 간선 존재
for x in range(1, 4):
    f[x, 0] = f[x-1, 0]
f[4, 0] = 0  # (4,0) 도로 없음

# 행 1~3
for y in range(1, 4):
    f[0, y] = f[0, y-1]  # 열 0은 아래에서만
    for x in range(1, 5):
        f[x, y] = 0
        if x > 0:
            f[x, y] += f[x-1, y]
        if y > 0:
            f[x, y] += f[x, y-1]

# 열 4의 세로 간선: (4,0) 없음
f[4, 0] = 0
f[4, 1] = f[3, 1] + f[4, 0]  # = 4 + 0 = 4
f[4, 2] = f[3, 2] + f[4, 1]  # = 10 + 4 = 14
f[4, 3] = f[3, 3] + f[4, 2]  # = 20 + 14 = 34

result = f[4, 3]
if result == 34:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')