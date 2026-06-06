from itertools import product

count = 0
for f_values in product(range(1, 6), repeat=5):
    f = {i+1: f_values[i] for i in range(5)}
    # 조건 (가): f(f(1)) = 4
    if f[f[1]] != 4:
        continue
    # 조건 (나): f(1) <= f(3) <= f(5)
    if not (f[1] <= f[3] <= f[5]):
        continue
    count += 1

if count == 115:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')