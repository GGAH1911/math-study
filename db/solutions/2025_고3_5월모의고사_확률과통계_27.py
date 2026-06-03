from itertools import permutations

valid_multisets = []
for a1 in range(6):
    for a2 in range(6):
        for a3 in range(6):
            for a4 in range(6):
                if a1 + a2 + a3 + a4 == 5:
                    product = (1**a1) * (2**a2) * (3**a3) * (4**a4)
                    if product == 96:
                        valid_multisets.append((a1, a2, a3, a4))

total = 0
for (a1, a2, a3, a4) in valid_multisets:
    cards = [1]*a1 + [2]*a2 + [3]*a3 + [4]*a4
    perms = set(permutations(cards))
    for perm in perms:
        if perm[-1] % 2 == 0:
            total += 1

print('total =', total)
if total == 52:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')