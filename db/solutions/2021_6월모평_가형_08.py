from math import factorial

# 원형 배열 (5개 객체)
circular_arrange = factorial(4)  # (5-1)!

# 1학년 내부 배열
group1_internal = factorial(2)

# 2학년 내부 배열
group2_internal = factorial(2)

# 전체 경우의 수
total = circular_arrange * group1_internal * group2_internal

# 검증
if total == 96:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')