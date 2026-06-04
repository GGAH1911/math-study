from itertools import permutations

def verify():
    cards = [0, 0, 1, 1, 1, 1, 1, 2, 2, 2]
    seen = set()
    count = 0
    for perm in permutations(cards):
        if perm in seen:
            continue
        seen.add(perm)
        transitions = sum(1 for k in range(9) if abs(perm[k+1] - perm[k]) == 2)
        if transitions == 3:
            count += 1
    if count == 144:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {count}')

verify()