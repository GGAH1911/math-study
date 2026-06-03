def verify():
    # a1 = 240
    a = [None, 240, None, None, None, None, None]
    for n in range(1, 6):
        if a[n] % n == 0:
            a[n+1] = a[n] // n
        else:
            a[n+1] = 3*a[n] + 1
    assert a[6] == 2, f'a1=240 failed: a6={a[6]}'
    
    # a1 = 26
    a = [None, 26, None, None, None, None, None]
    for n in range(1, 6):
        if a[n] % n == 0:
            a[n+1] = a[n] // n
        else:
            a[n+1] = 3*a[n] + 1
    assert a[6] == 2, f'a1=26 failed: a6={a[6]}'
    
    # a1 = 18
    a = [None, 18, None, None, None, None, None]
    for n in range(1, 6):
        if a[n] % n == 0:
            a[n+1] = a[n] // n
        else:
            a[n+1] = 3*a[n] + 1
    assert a[6] == 2, f'a1=18 failed: a6={a[6]}'
    
    total = 240 + 26 + 18
    assert total == 284, f'Sum failed: {total}'
    print('VERIFY_PASS')

verify()