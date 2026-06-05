from fractions import Fraction
import numpy as np

# 검증: 면적 비율이 9/20인지 확인
r_squared = (6 * np.sqrt(10) / 5) ** 2
OB1_squared = 32
ratio = r_squared / OB1_squared
print(f'면적 비율: {ratio} (기댓값: {9/20})')
assert abs(ratio - 9/20) < 1e-10, 'VERIFY_FAIL'

# 무한급수 검증
S1 = 4
common_ratio = Fraction(9, 20)
result = S1 / (1 - common_ratio)
expected = Fraction(80, 11)

print(f'무한급수 합: {result} (기댓값: {expected})')
assert result == expected, 'VERIFY_FAIL'

print('VERIFY_PASS')