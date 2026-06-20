from itertools import product

# 조건을 만족하는 경우를 직접 세기
count = 0
total = 0

for a, b in product(range(1, 7), repeat=2):
    total += 1
    # 조건: |a-3| + |b-3| = 2 또는 a = b
    if abs(a - 3) + abs(b - 3) == 2 or a == b:
        count += 1

probability = count / total
expected = 1 / 3

if abs(probability - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {probability}, expected {expected}')