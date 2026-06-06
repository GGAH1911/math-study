def verify():
    a = {}
    a[0] = 0
    a[1] = -1
    
    def compute_a(n):
        if n in a:
            return a[n]
        if n % 2 == 0:
            a[n] = 2 * compute_a(n // 2) + 1
        else:
            a[n] = 2 * compute_a(n // 2) + 2
        return a[n]
    
    # 조건 검증
    if compute_a(7) != 2:
        print('VERIFY_FAIL')
        return
    
    # 답 검증
    result = compute_a(25)
    if result == 8:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()