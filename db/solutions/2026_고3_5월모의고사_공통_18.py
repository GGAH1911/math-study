import math

# 원래 방정식: log_2(x-4) = log_{1/2}(x-6) + 3
# 답: x = 8

x = 8

# 좌변: log_2(x-4)
left_side = math.log2(x - 4)

# 우변: log_{1/2}(x-6) + 3
# log_{1/2}(a) = log(a) / log(1/2) = log(a) / (-log(2)) = -log_2(a)
right_side = -math.log2(x - 6) + 3

if abs(left_side - right_side) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')