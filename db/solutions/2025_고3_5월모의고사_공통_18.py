# 주어진 조건 검증
# 조건 1: sum(a_k + 3) = 30
# 조건 2: sum(2*a_k + b_k) = 53
# 구하는 것: sum(b_k) = ?

sum_a = 15  # 조건 1에서 도출
sum_b = 23  # 우리의 답

# 조건 1 검증
cond1 = sum_a + 5 * 3
print(f'조건 1 검증: sum(a_k + 3) = {sum_a} + 15 = {cond1} (should be 30)')
assert cond1 == 30, f'조건 1 실패: {cond1} != 30'

# 조건 2 검증
cond2 = 2 * sum_a + sum_b
print(f'조건 2 검증: 2*sum(a_k) + sum(b_k) = 2*{sum_a} + {sum_b} = {cond2} (should be 53)')
assert cond2 == 53, f'조건 2 실패: {cond2} != 53'

print('VERIFY_PASS')