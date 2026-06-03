import math
sigma = 16
n = 64
z = 1.96
lower_given = 240.12
margin = z * sigma / math.sqrt(n)
x_bar = lower_given + margin
a = x_bar + margin
result = x_bar + a
expected = 492
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
