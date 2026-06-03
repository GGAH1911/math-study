from itertools import permutations

count = 0
# 1을 기준 위치에 고정하여 회전 동치 처리
others = [2, 3, 4, 5, 6]
for perm in permutations(others):
    arrangement = [1] + list(perm)
    n = len(arrangement)
    valid = True
    for i in range(n):
        s = arrangement[i] + arrangement[(i + 1) % n]
        if s == 11:
            valid = False
            break
    if valid:
        count += 1

if count == 72:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')