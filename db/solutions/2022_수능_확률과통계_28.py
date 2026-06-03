from itertools import product
import math

X = [1, 2, 3, 4, 5]
Y = [1, 2, 3, 4]

count = 0
for vals in product(Y, repeat=5):
    f = dict(zip(X, vals))
    # 조건 (가): f(x) >= sqrt(x)
    if not all(f[x] >= math.sqrt(x) for x in X):
        continue
    # 조건 (나): |치역| = 3
    if len(set(f[x] for x in X)) == 3:
        count += 1

if count == 128:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')