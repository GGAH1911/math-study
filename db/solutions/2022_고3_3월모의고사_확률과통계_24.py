from itertools import permutations

digits = [1, 1, 2, 2, 2, 3]
all_perms = set(permutations(digits))
odd_count = sum(1 for p in all_perms if p[-1] % 2 == 1)

expected = 30
if odd_count == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {odd_count}, expected {expected}')