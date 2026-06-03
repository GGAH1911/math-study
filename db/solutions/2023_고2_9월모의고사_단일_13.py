def verify():
    a = [0, 2]  # a[0] unused, a[1] = 2
    for n in range(1, 16):
        if a[n] < 8:
            a.append(2 * a[n] - 1)
        else:
            a.append(a[n] // 3)
    total = sum(a[1:])
    expected = 87
    if total == expected:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
verify()