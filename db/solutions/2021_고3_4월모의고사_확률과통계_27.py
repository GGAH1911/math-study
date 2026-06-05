import math

n = 5
f_value = sum(math.comb(2*n+1, 2*k) for k in range(1, n+1))

if f_value == 1023:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')