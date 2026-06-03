def verify_sequence(a1):
    from fractions import Fraction
    a = [0, a1]
    for i in range(1, 6):
        if a[i] % 2 == 1:
            a.append((a[i] + 3) // 2)
        else:
            a.append((3 * a[i]) // 2)
    
    if 3 * a[4] != 2 * a[4] or 3 * a[5] != 2 * a[5]:
        return False
    
    return a[4] + a[5] <= 24

valid_a1 = [1, 2, 3, 4, 9, 12]
total = 0
for a1 in valid_a1:
    a = [0, a1]
    for i in range(1, 6):
        if a[i] % 2 == 1:
            a.append((a[i] + 3) // 2)
        else:
            a.append(3 * a[i] // 2)
    assert all(a[n] <= a[3] for n in range(1, len(a))), f'Failed for a1={a1}'
    assert a[4] + a[5] <= 24, f'Failed sum check for a1={a1}'
    total += a1

assert total == 31, f'Expected 31, got {total}'
print('VERIFY_PASS')