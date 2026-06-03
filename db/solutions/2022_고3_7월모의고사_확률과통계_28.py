from itertools import product as iproduct
import math

X = [1,2,3,4,5,6]
Y = [1,2,3,4,5]

count = 0
for vals in iproduct(Y, repeat=6):
    # condition (나): non-decreasing
    if any(vals[i] > vals[i+1] for i in range(5)):
        continue
    # condition (가): sqrt(f(1)*f(2)*f(3)) is natural number
    prod = vals[0] * vals[1] * vals[2]
    sqrt_val = math.isqrt(prod)
    if sqrt_val * sqrt_val == prod:
        count += 1

if count == 87:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')
