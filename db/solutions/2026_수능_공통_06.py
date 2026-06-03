import math
a = 3**(1/4)
b = 3**(3/4)
ab = a * b
log_a_b = math.log(b) / math.log(a)
log_3_b_div_a = math.log(b/a) / math.log(3)
log_9_ab = math.log(ab) / math.log(9)
assert abs(log_a_b - 3) < 1e-10, f'log_a b = {log_a_b}'
assert abs(log_3_b_div_a - 0.5) < 1e-10, f'log_3(b/a) = {log_3_b_div_a}'
assert abs(log_9_ab - 0.5) < 1e-10, f'log_9(ab) = {log_9_ab}'
print('VERIFY_PASS')