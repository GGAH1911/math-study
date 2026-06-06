# 원래 문제 조건 검증
# 조건 1: sum(2*a_k - b_k) = 80
# 조건 2: sum(b_k) = 30
# 구한 답: sum(a_k) = 55

sum_a = 55
sum_b = 30

# 조건 1 검증
condition_1 = 2 * sum_a - sum_b
if condition_1 == 80:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')