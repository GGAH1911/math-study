from itertools import product
count = 0
for vals in product(range(1,7), repeat=6):
    f = {i+1: vals[i] for i in range(6)}
    # Condition (가)
    if not (f[1] <= f[2] <= f[3] <= f[4] <= 5):
        continue
    # Condition (나)
    if f[f[4]] == 4 and f[f[5]] == 5 and f[f[6]] == 6:
        count += 1
if count == 75:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')