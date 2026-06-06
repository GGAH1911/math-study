def verify():
    # 수열 생성
    a = [0] * 101
    a[1] = 9
    a[2] = 3
    for n in range(1, 99):
        a[n+2] = a[n+1] - a[n]
    
    # |a_k| = 3을 만족하는 k 찾기
    count = 0
    valid_k = []
    for k in range(1, 101):
        if abs(a[k]) == 3:
            count += 1
            valid_k.append(k)
    
    # 답 검증
    if count == 33:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()