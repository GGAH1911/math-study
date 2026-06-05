from itertools import product

count = 0
for a, b, c in product(range(1, 7), repeat=3):
    if (a-2)**2 + (b-3)**2 + (c-4)**2 == 2:
        count += 1

total = 6**3
probability = count / total

if abs(probability - 1/18) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')