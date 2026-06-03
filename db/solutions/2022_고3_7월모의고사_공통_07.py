def verify():
    a = [0] * 21
    a[1] = 1/2
    
    for n in range(1, 20):
        if a[n] < 0:
            a[n+1] = a[n] + 1
        else:
            a[n+1] = -2*a[n] + 1
    
    result = a[10] + a[20]
    expected = -1
    
    if abs(result - expected) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()