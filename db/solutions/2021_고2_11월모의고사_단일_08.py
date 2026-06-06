import math

a = 81
log2_3 = math.log(3, 2)
log_a_4 = math.log(4, a)
product = log2_3 * log_a_4

if abs(product - 0.5) < 1e-9:
    log3_a = math.log(a, 3)
    if abs(log3_a - 4) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')