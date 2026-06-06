import math

# 주어진 값
W = 15
S = 186
C = 75
a = 6

# 채널용량 공식으로 검증
C_calculated = W * math.log2(1 + S/a)

if abs(C_calculated - C) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')