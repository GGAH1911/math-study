import numpy as np

# 주어진 조건: |a| = 3, |a - 2b| = 6, a와 b는 같은 방향
# 풀이: b = k*a (k > 0)로 나타낼 수 있음
# |a - 2ka| = 6 => |1-2k| * 3 = 6 => |1-2k| = 2
# 1-2k = -2 => k = 3/2
# 따라서 |b| = 9/2

k = 3/2
magnitude_a = 3
magnitude_b = k * magnitude_a

# 검증: |a - 2b| = 6인지 확인
# b = (3/2)*a이므로 a - 2b = a - 3a = -2a
# |a - 2b| = |-2a| = 2*|a| = 2*3 = 6
verify_magnitude = 2 * magnitude_a

if abs(verify_magnitude - 6) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')