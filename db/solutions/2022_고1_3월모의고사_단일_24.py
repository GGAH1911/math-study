# 오각형 내각의 합 검증
angles = {
    'A': 105,
    'B': None,  # x
    'C': None,  # y
    'D': 109,
    'E': 92
}

# x + y = 234일 때 내각의 합이 540인지 확인
x_plus_y = 234
known_sum = 105 + 109 + 92  # 306
total_sum = known_sum + x_plus_y

# 오각형 내각의 합
pentagon_interior_sum = (5 - 2) * 180

if total_sum == pentagon_interior_sum:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')