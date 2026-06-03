import math

# 계산된 답: 16
answer = 16

# 망원급수 검증
total = 0
for k in range(1, 81):
    x_k = math.sqrt(k) / 2
    x_k1 = math.sqrt(k + 1) / 2
    term = 1 / (x_k + x_k1)
    total += term

if abs(total - 16) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')