from itertools import permutations

original = [1, 1, 2, 2, 2, 3, 3, 4]

def is_valid(arrangement):
    for i in range(len(arrangement)-1):
        if arrangement[i] * arrangement[i+1] % 2 == 1:
            return False
    return True

count = 0
seen_multisets = set()

for remove_idx in range(len(original)):
    remaining = original[:remove_idx] + original[remove_idx+1:]
    remaining_key = tuple(sorted(remaining))
    if remaining_key in seen_multisets:
        continue
    seen_multisets.add(remaining_key)
    seen_perms = set()
    for perm in permutations(remaining):
        if perm not in seen_perms:
            seen_perms.add(perm)
            if is_valid(perm):
                count += 1

print('VERIFY_PASS' if count == 264 else 'VERIFY_FAIL')