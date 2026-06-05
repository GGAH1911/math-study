from itertools import permutations

def is_valid_circular_arrangement(arrangement):
    n = 8
    for classroom in range(4):
        positions = [i for i, s in enumerate(arrangement) if s[0] == classroom]
        idx1, idx2 = positions
        if abs(idx1 - idx2) == 1 or abs(idx1 - idx2) == n - 1:
            continue
        else:
            return False
    return True

first_student = (0, 0)
remaining_students = [(i, j) for i in range(4) for j in range(2) if not (i == 0 and j == 0)]

valid_count = 0
for perm in permutations(remaining_students):
    arrangement = [first_student] + list(perm)
    if is_valid_circular_arrangement(arrangement):
        valid_count += 1

if valid_count == 96:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')