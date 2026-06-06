import math

a = 3
k_squared = 135/4
k = math.sqrt(k_squared)

# 첫 번째 쌍곡선 검증: P(9/2, k)가 x^2/9 - y^2/27 = 1 위에 있는지
verify1 = (9/2)**2 / 9 - k**2 / 27
print(f'First hyperbola check (should be 1): {verify1}')

# a' = 2a^2/9 = 2 확인
a_prime = 2 * (a**2) / 9
print(f'a\' (should be 2): {a_prime}')

# 최종 답 검증
answer = 4 * (a**2 + k_squared)
print(f'4(a^2 + k^2) = {answer}')

if abs(verify1 - 1.0) < 1e-10 and abs(a_prime - 2.0) < 1e-10 and answer == 171:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')