from itertools import permutations

available = {101, 103, 104, 105, 201, 202, 203, 205}

count = 0
for A in available:
    for B in available:
        if B == A:
            continue
        # Condition (나)
        if abs(A - B) not in (1, 100):
            continue
        for C in available:
            if C == A or C == B:
                continue
            # Condition (다)
            diff_ac = abs(A - C)
            if diff_ac <= 4 or diff_ac == 100:
                continue
            # Remaining 2 tourists choose from remaining 5 rooms
            remaining = available - {A, B, C}
            count += len(remaining) * (len(remaining) - 1)

print('VERIFY_PASS' if count == 920 else f'VERIFY_FAIL: got {count}')
