def verify():
    # 주어진 관계식: a_{2n} = sum_{k=1}^{2n-1}(k - a_k)
    # 검증: sum_{k=1}^{10} a_k = 45
    
    # 홀수 항은 자유도이므로 0으로 설정하고 짝수 항을 관계식으로 계산
    a = {}
    for k in [1, 3, 5, 7, 9]:
        a[k] = 0
    
    # 관계식 a_{2n} = sum_{k=1}^{2n-1}(k - a_k)로부터 짝수 항 계산
    for n in range(1, 6):
        a[2*n] = sum(k - a.get(k, 0) for k in range(1, 2*n))
    
    # 검증 1: 원본 관계식 만족 확인
    for n in range(1, 6):
        lhs = a[2*n]
        rhs = sum(k - a[k] for k in range(1, 2*n))
        if abs(lhs - rhs) > 1e-9:
            print('VERIFY_FAIL')
            return
    
    # 검증 2: sum_{k=1}^{10} a_k = 45 확인
    total = sum(a[k] for k in range(1, 11))
    if abs(total - 45) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()