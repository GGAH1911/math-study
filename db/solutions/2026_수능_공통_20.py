def verify():
    a = [0, 7, 10]
    for n in range(2, 12):
        a.append(n - 2 * a[n])
    for n in range(2, 13):
        sum_n = sum(a[1:n+1])
        expected = (2/3) * a[n] + (1/6) * n**2 - (1/6) * n + 10
        if abs(sum_n - expected) > 1e-9:
            print('VERIFY_FAIL')
            return
    sum_12 = sum(a[1:13])
    sum_odd = a[3] + a[5] + a[7] + a[9] + a[11]
    result = sum_12 + sum_odd
    if result == 52 and (10 * 52) // 4 == 130:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
verify()