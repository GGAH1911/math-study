# 원래 문제의 조건 검증
a_15 = 37
sum_1_to_15 = 5  # 첫 번째 조건에서 도출
sum_1_to_14 = sum_1_to_15 - a_15

# 조건 1 검증: sum(3*a_k + 2) = 45
# 이는 3*sum(a_k) + 30 = 45를 의미
cond1_left = 3 * sum_1_to_15 + 30
print(f'Condition 1: 3*5 + 30 = {cond1_left}, expected 45: {cond1_left == 45}')

# 조건 2 검증: 2*sum(a_k for k=1..15) = 42 + sum(a_k for k=1..14)
cond2_left = 2 * sum_1_to_15
cond2_right = 42 + sum_1_to_14
print(f'Condition 2: 2*5 = {cond2_left}, 42 + {sum_1_to_14} = {cond2_right}: {cond2_left == cond2_right}')

if cond1_left == 45 and cond2_left == cond2_right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')