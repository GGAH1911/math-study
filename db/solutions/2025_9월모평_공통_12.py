import numpy as np
a1, d = -4, 2
def compute_b(n):
    total = 0
    for k in range(1, n+1):
        ak = a1 + (k-1)*d
        total += ((-1)**(k+1)) * ak
    return total

b2 = compute_b(2)
b3 = compute_b(3)
b7 = compute_b(7)

if abs(b2 - (-2)) < 1e-9 and abs(b3 + b7) < 1e-9:
    sum_b = sum(compute_b(n) for n in range(1, 10))
    if abs(sum_b - (-20)) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')