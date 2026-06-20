from itertools import product

a_values = [1, 3, 5, 7]
b_values = [4, 6, 8, 10]

count = 0
for a, b in product(a_values, b_values):
    ratio = b / a
    if 1 < ratio < 4:
        count += 1

total = len(a_values) * len(b_values)
probability = count / total

print(f'{count}/{total} = {probability}')
if abs(probability - 9/16) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')