import math
m, n = 27, 81
log_n_4 = math.log(4) / math.log(n)
log_m_2 = math.log(2) / math.log(m)
log_2_n = math.log(n) / math.log(2)
result = log_n_4 * (4 / log_m_2 + log_2_n)
if abs(result - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')