import numpy as np
from scipy.optimize import fsolve

# 경우 2-1: r = 2/3, m = 1
r = 2/3
m = 1
b1 = 9 * m

# 등비수열 합 확인
geometric_sum = b1 / (1 - r)
print(f'등비급수 합: {geometric_sum}')

# 부분합 계산 (충분히 많은 항)
partial_sum = 0
for n in range(1, 100):
    bn = b1 * (r ** (n - 1))
    an = m * (10 - n)
    cos_term = np.cos(an * np.pi)
    partial_sum += bn * cos_term

print(f'부분합 (n=1..99): {partial_sum}')
print(f'이론값 -27/5 = {-27/5}')
print(f'절댓값: {abs(partial_sum)}')
print(f'10m = {10 * abs(partial_sum)}')

if abs(abs(partial_sum) - 27/5) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')