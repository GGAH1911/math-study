from itertools import product

# 가능한 구성 목록: (검, 파, 빨)
configs = []

# 검=0, 파+빨=5인 경우
for p in range(5):
    r = 5 - p
    if 0 <= p <= 4 and 0 <= r <= 4:
        configs.append((0, p, r))

# 검=1, 파+빨=4인 경우
for p in range(5):
    r = 4 - p
    if 0 <= p <= 4 and 0 <= r <= 4:
        configs.append((1, p, r))

total = 0
for c, p, r in configs:
    # 각 구성에 대해 2명에게 분배하는 경우의 수
    ways = (c + 1) * (p + 1) * (r + 1)
    total += ways

if total == 114:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')