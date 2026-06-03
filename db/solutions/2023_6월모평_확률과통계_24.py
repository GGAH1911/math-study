from itertools import product

A = [1, 2, 3]
B = [1, 2, 3, 4, 5]

count_diff_1 = 0
total_cases = 0

for a in A:
    for b in B:
        total_cases += 1
        if abs(a - b) == 1:
            count_diff_1 += 1

probability = count_diff_1 / total_cases
expected = 1/3

if abs(probability - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')