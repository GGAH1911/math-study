from itertools import product
X = [1, 2, 3, 4, 5]
Y = [1, 2, 3, 4]
count = 0
for f_values in product(Y, repeat=len(X)):
    is_non_decreasing = all(f_values[i] <= f_values[i+1] for i in range(len(f_values)-1))
    if not is_non_decreasing:
        continue
    codomain = set(f_values)
    if 1 in codomain and 3 in codomain:
        count += 1
if count == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')