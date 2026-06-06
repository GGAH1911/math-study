import math
k = 12
g_0 = k
g_3 = k - 9
max_f = math.log(g_0) / math.log(3)
min_f = math.log(g_3) / math.log(3)
sum_extrema = max_f + min_f
expected_sum = 2 + math.log(4) / math.log(3)
if abs(sum_extrema - expected_sum) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')