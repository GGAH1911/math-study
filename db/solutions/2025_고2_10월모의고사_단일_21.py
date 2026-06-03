import numpy as np

def get_zeros(a):
    zeros = []
    if 0 < a < 8:
        x1 = np.log2(float(a)) - 3
        zeros.append(x1)
    if -52 <= a < 12:
        x2 = 6 - np.log2(float(12 - a))
        if x2 >= 0:
            zeros.append(x2)
    return sorted(zeros)

valid_a = []
for a in range(-200, 200):
    zeros = get_zeros(a)
    if len(zeros) == 2:
        x1, x2 = zeros
        k = x2 - x1
        if 0 < k <= 4:
            all_roots = sorted([x1, x2, x1 + k, x2 + k])
            distinct = [all_roots[0]]
            for r in all_roots[1:]:
                if abs(r - distinct[-1]) > 1e-9:
                    distinct.append(r)
            if len(distinct) == 3:
                valid_a.append(a)

total = sum(valid_a)
print(f'Valid integers: {valid_a}')
print(f'Sum = {total}')
if total == 22:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')