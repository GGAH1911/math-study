import sympy as sp

# 주어진 조건: sum_{k=1}^{4}(2a_k - k) = 0
# 이를 전개하면: 2*sum(a_k) - sum(k) = 0

sum_k = sum(range(1, 5))  # sum_{k=1}^{4} k
print(f'sum(k from 1 to 4) = {sum_k}')

# 조건식: 2*sum(a_k) - sum_k = 0
# sum(a_k) = sum_k / 2
sum_a_k = sum_k / 2
print(f'sum(a_k) = {sum_a_k}')

# 검증: 조건식이 0이 되는지 확인
verification = 2 * sum_a_k - sum_k
print(f'2*sum(a_k) - sum(k) = {verification}')

if abs(verification) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')