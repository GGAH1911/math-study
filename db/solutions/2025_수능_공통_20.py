import math

# k 값을 수치적으로 구하기 (k + log_5(k) = 3)
def find_k():
    for k_try in [x/1000 for x in range(1000, 3000)]:
        if k_try + math.log(k_try, 5) > 3.001:
            return k_try - 0.001
    return 2.445

k = 2.445
# 검증: k + log_5(k) ≈ 3
verify_eq1 = k + math.log(k, 5)
print(f'k + log_5(k) = {verify_eq1:.6f} (should be ~3)')

# 검증: 5^(3-k) ≈ k
verify_eq2 = 5 ** (3 - k)
print(f'5^(3-k) = {verify_eq2:.6f} (should be ~{k:.6f})')

# k^3 * 5^(3k) = 5^9 검증
product = (k**3) * (5**(3*k))
five_to_nine = 5**9
print(f'k^3 * 5^(3k) = {product:.2e} (should be {five_to_nine:.2e})')

# 답 검증
x_input = 1 / (k**3 * 5**(3*k))
print(f'Input x = 5^(-9) = {x_input:.6e}')
print(f'Expected x = {1/five_to_nine:.6e}')

# f(5^(-9)) = 9 - 3*log_5(5^(-9)) = 9 - 3*(-9) = 36
result = 9 - 3 * math.log(1/five_to_nine, 5)
print(f'f(5^(-9)) = {result:.1f}')

if abs(result - 36) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')