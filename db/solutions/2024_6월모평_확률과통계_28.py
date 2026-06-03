from itertools import product

X = [1, 2, 3, 4, 5]
count = 0

for f1, f2, f3, f4, f5 in product(X, repeat=5):
    # (가) f(1)*f(3)*f(5) 홀수
    if (f1 * f3 * f5) % 2 == 0:
        continue
    # (나) f(2) < f(4)
    if f2 >= f4:
        continue
    # (다) 치역 원소 수 = 3
    if len({f1, f2, f3, f4, f5}) != 3:
        continue
    count += 1

if count == 144:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')