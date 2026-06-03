import math
a = 81 ** (1/3)  # 실수 세제곱근 (81 > 0이므로 유일)
result = math.log(a, 9)
expected = 2/3
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')