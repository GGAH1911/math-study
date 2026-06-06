# 검증: 주어진 조건을 만족하는지 확인
# a_k, b_k의 합을 구함

sum_a = 17  # 조건 (2)에서: sum_a - sum_b = 3, sum_b = 14이므로 sum_a = 17
sum_b = 14  # 유도한 값

# 조건 1 확인: sum(a_k + 2*b_k) = 45
condition_1 = sum_a + 2 * sum_b
print(f'조건 1: {condition_1} = 45, 확인: {condition_1 == 45}')

# 조건 2 확인: sum(a_k - b_k) = 3
condition_2 = sum_a - sum_b
print(f'조건 2: {condition_2} = 3, 확인: {condition_2 == 3}')

# 답 계산
answer = sum_b - 10 * (1/2)
print(f'답: {answer}')

if condition_1 == 45 and condition_2 == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')