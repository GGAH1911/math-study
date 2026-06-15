from itertools import permutations

cards = [1, 2, 3, 6, 18]
count = 0
valid_perms = []

for perm in permutations(cards):
    valid = True
    for i in range(4):
        product = perm[i] * perm[i+1]
        if product % 6 != 0:
            valid = False
            break
    if valid:
        count += 1
        valid_perms.append(perm)

p = 0
for perm in permutations(cards):
    for i in range(4):
        if (perm[i] == 1 and perm[i+1] == 2) or (perm[i] == 2 and perm[i+1] == 1):
            p += 1
            break

q = 0
for perm in permutations(cards):
    for i in range(4):
        if (perm[i] == 1 and perm[i+1] == 3) or (perm[i] == 3 and perm[i+1] == 1):
            if (perm[i] == 1 and perm[i+1] == 2) or (perm[i] == 2 and perm[i+1] == 1):
                q += 1
            break

q = 0
for perm in permutations(cards):
    has_12 = False
    has_13 = False
    for i in range(4):
        if (perm[i] == 1 and perm[i+1] == 2) or (perm[i] == 2 and perm[i+1] == 1):
            has_12 = True
        if (perm[i] == 1 and perm[i+1] == 3) or (perm[i] == 3 and perm[i+1] == 1):
            has_13 = True
    if has_12 and has_13:
        q += 1

r = count
result = 48 + 12 + 36

if result == 96:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')