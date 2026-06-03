import numpy as np

def count_real_nth_roots(a, n):
    if n % 2 == 1:
        return 1  # odd n: always 1 real nth root
    else:
        if a > 0:
            return 2
        elif a == 0:
            return 1
        else:
            return 0

total = 0
for n in range(2, 11):
    a = np.sin(n * np.pi / 5)
    # treat near-zero as zero
    if abs(a) < 1e-10:
        a = 0.0
    fn = count_real_nth_roots(a, n)
    total += fn

if total == 9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}')
