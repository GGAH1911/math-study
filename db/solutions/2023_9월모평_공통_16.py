import math

x = 7

# 원래 방정식: log_3(x-4) = log_9(x+2)
left = math.log(x - 4) / math.log(3)
right = math.log(x + 2) / math.log(9)

if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')