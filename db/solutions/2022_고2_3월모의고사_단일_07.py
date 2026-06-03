from itertools import permutations

cards = [1, 2, 3, 4, 5]
count = 0
for perm in permutations(cards):
    # 짝수 카드끼리 이웃하지 않는지 확인
    valid = True
    for i in range(len(perm) - 1):
        if perm[i] % 2 == 0 and perm[i+1] % 2 == 0:
            valid = False
            break
    if valid:
        count += 1

if count == 72:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')
