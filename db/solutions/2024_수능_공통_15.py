def verify_sequence(a1):
    a = [0, a1]
    for n in range(1, 7):
        if a[n] % 2 == 1:
            a.append(2 ** a[n])
        else:
            a.append(a[n] // 2)
    return a[6] + a[7] == 3

valid_a1 = [1, 2, 3, 4, 5, 6, 8, 12, 16, 32, 64]
all_valid = all(verify_sequence(a) for a in valid_a1)
total_sum = sum(valid_a1)

if all_valid and total_sum == 153:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')