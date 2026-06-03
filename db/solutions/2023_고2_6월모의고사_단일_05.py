import math

# 원래 함수: log 619
N = 619
expected = 2.7917

# 계산
actual = math.log10(N)

# 검증 (소수점 4자리까지)
if abs(actual - expected) < 0.00005:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {expected}, Actual: {actual}')