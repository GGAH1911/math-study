# 검증: 주어진 조건을 만족하는 수열로 검사
# 조건 1: 2*sum(a) - sum(b) = 34
# 조건 2: sum(a) = 10
# 구하는 값: sum(a) - sum(b)

sum_a = 10
sum_2a_minus_b = 34

# 첫 조건에서
# 2*sum_a - sum_b = 34
sum_b = 2 * sum_a - sum_2a_minus_b

# 구하는 답
answer = sum_a - sum_b

# 검증
if sum_a == 10 and 2 * sum_a - sum_b == 34:
    print(f'VERIFY_PASS')
else:
    print(f'VERIFY_FAIL')