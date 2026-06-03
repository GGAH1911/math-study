import numpy as np

sqrt_2 = np.sqrt(2)

# 원래 기수와 지수 (이미지의 원래 식)
base = 4 / (2 ** sqrt_2)
exponent = 2 + sqrt_2

# 직접 계산
result_direct = base ** exponent

# 원래 문제의 식으로 검증
# (4 / 2^sqrt(2))^(2+sqrt(2)) 계산
print('Direct calculation:', result_direct)
print('Is close to 4:', np.isclose(result_direct, 4, rtol=1e-10))

# 지수 계산으로도 검증
numerator_exp = 2 * (2 + sqrt_2)
denominator_exp = sqrt_2 * (2 + sqrt_2)
result_exp = numerator_exp - denominator_exp
result_from_exponent = 2 ** result_exp

print('Via exponent calculation:', result_from_exponent)
print('Exponent value:', result_exp)

if np.isclose(result_direct, 4, rtol=1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')