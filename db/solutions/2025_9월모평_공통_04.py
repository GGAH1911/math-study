# 그래프에서 읽은 극한값 검증
# x < 0 부분: (-2, 2)에서 (0, -2)로 향하는 곡선 → lim_{x→0-} f(x) = -2
# x > 1 부분: (1, 1)의 실선원(채워진 점)에서 시작 → lim_{x→1+} f(x) = 1

limit_0_minus = -2  # 그래프: 좌측 곡선이 y = -2로 접근
limit_1_plus = 1    # 그래프: (1, 1)의 채워진 점에서 우측 곡선 시작

answer_sum = limit_0_minus + limit_1_plus

if answer_sum == -1:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")