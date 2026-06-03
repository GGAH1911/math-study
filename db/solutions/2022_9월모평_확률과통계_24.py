from itertools import product

A = [1, 3, 5, 7]
B = [2, 4, 6, 8]

count = 0
for a, b in product(A, B):
    if a * b > 31:
        count += 1

total = len(A) * len(B)
prob = count / total

if abs(prob - 3/16) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')