# 주어진 조건 검증
# 조건 1: sum(3*a_k + 5) = 55에서 sum(a_k) = 10을 유도
sum_a = 10
condition1_check = 3 * sum_a + 5 * 5
print(f'조건1 확인: 3*{sum_a} + 25 = {condition1_check} (목표: 55)')
assert condition1_check == 55, 'Condition 1 failed'

# 조건 2: sum(a_k + b_k) = 32에서 sum(b_k)를 구함
sum_b = 22
condition2_check = sum_a + sum_b
print(f'조건2 확인: {sum_a} + {sum_b} = {condition2_check} (목표: 32)')
assert condition2_check == 32, 'Condition 2 failed'

print('VERIFY_PASS')