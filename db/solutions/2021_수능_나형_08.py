from itertools import product
count = 0
for a, b, c in product(range(1, 7), repeat=3):
    if a * b * c == 4:
        count += 1
total = 6**3
prob = count / total
if abs(prob - 1/36) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')