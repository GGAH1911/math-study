import math
result = math.log10(0.183)
expected = -0.7375
# 표에서 읽은 log1.83 = 0.2625 (반올림된 값)이므로 허용 오차 0.001
if abs(result - expected) < 0.001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: math.log10(0.183)={result:.6f}, expected={expected}')