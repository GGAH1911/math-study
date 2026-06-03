def f(x):
    # x < 0: 왼쪽 선분, x -> 0- 일 때 y -> 4
    # 기울기는 임의지만 (0,4)에 빈 점으로 수렴
    if x < 0:
        # 예: y = 4 + x (기울기 1) 로 모델링하면 x->0- 일 때 4로 접근
        return 4 + x
    # 0 < x <= 2: (0,1) 빈 점에서 (2,3) 채워진 점으로 가는 직선 y = 1 + x
    if 0 < x <= 2:
        return 1 + x
    # x > 2: y = 2 수평선
    if x > 2:
        return 2
    # x = 0: 채워진 점 (0, 2)
    if x == 0:
        return 2

# 좌극한 x->0-
left_limit = None
for n in range(1, 8):
    left_limit = f(-10**(-n))
# 마지막 값 ~ 4

# 우극한 x->2+
right_limit = None
for n in range(1, 8):
    right_limit = f(2 + 10**(-n))

total = round(left_limit + right_limit, 6)
if abs(total - 6) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
