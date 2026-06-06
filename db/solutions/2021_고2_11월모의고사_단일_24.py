import math

x = 11

# 원래 방정식: 2*log_4(x-3) + log_2(x-10) = 3
left_side = 2 * math.log(x - 3, 4) + math.log(x - 10, 2)
right_side = 3

if abs(left_side - right_side) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')