from math import comb

# 빨간색 5개를 4명에게 나누어 주는 경우의 수
red_cases = comb(4 + 5 - 1, 5)  # C(8, 5)

# 파란색 2개를 4명에게 나누어 주는 경우의 수
blue_cases = comb(4 + 2 - 1, 2)  # C(5, 2)

# 전체 경우의 수
total = red_cases * blue_cases

if total == 560:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')