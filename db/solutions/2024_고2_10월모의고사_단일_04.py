# 그래프 읽기 문제: 극한값의 합 검증
# 그래프에서 읽은 극한값들
lim_left_neg1 = 3  # x → -1⁻일 때
lim_right_0 = 1    # x → 0⁺일 때
result = lim_left_neg1 + lim_right_0
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')