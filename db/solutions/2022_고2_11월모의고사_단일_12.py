# 조건을 만족하는 수열 구성 후 검증
a = [0] * 11
a[1] = 1
a[10] = 4

# a_2부터 a_9까지의 합이 10이 되도록 설정
for k in range(2, 10):
    a[k] = 10 / 8

# 원래 조건 검증: ∑(a_k + a_{k+1}) = 25
sum_condition = sum(a[k] + a[k+1] for k in range(1, 10))
condition_satisfied = abs(sum_condition - 25) < 1e-10

# 최종 답 검증: ∑a_k = 15
total_sum = sum(a[1:11])
answer_correct = abs(total_sum - 15) < 1e-10

if condition_satisfied and answer_correct:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')