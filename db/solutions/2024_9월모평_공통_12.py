def compute_sequence(a1, steps):
    a = a1
    for _ in range(steps):
        if a % 2 == 1:  # odd
            a = a + 1
        else:  # even
            a = a // 2
    return a

candidates = [25, 31, 52, 64]
valid = True

for a1 in candidates:
    a2 = compute_sequence(a1, 1)
    a4 = compute_sequence(a1, 3)
    if a2 + a4 != 40:
        valid = False
        break

if valid and sum(candidates) == 172:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')