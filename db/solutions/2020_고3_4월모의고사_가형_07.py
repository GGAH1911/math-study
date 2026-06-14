from itertools import permutations

def check_a_not_adjacent(perm):
    for i in range(len(perm)-1):
        if perm[i] == 'a' and perm[i+1] == 'a':
            return False
    return True

s = 'aabbcc'
valid_count = 0
seen = set()

for perm in permutations(s):
    if perm not in seen:
        seen.add(perm)
        if check_a_not_adjacent(perm):
            valid_count += 1

if valid_count == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')