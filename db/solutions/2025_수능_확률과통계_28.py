from itertools import product as iproduct

X = [1, 2, 3, 4, 5, 6]
divisors_of_6 = {1, 2, 3, 6}

count = 0
for f1, f2, f3, f4, f5, f6 in iproduct(X, repeat=6):
    if f1 * f6 not in divisors_of_6:
        continue
    if 2*f1 <= f2 <= f3 <= f4 <= f5 <= 2*f6:
        count += 1

if count == 171:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')