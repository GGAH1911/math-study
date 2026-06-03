from itertools import permutations

cards = [1, 2, 2, 3, 3, 3]

def distinct_perms(lst):
    seen = set()
    for p in permutations(lst):
        if p not in seen:
            seen.add(p)
            yield p

count = 0
for perm in distinct_perms(cards):
    valid = all(perm[i] + perm[i+1] >= 4 for i in range(len(perm)-1))
    if valid:
        count += 1

if count == 24:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')