# 서로 다른 a_1 값들에 대해 조건 만족과 답 검증
for a1_val in [0, 5, -3, 10]:
    a = [None] * 23
    a[1] = a1_val
    
    # 조건식 a_n + a_{n+1} = 2n을 이용해 수열 구성
    for n in range(1, 22):
        a[n + 1] = 2 * n - a[n]
    
    # 원래 조건 검증
    for n in range(1, 22):
        if a[n] + a[n + 1] != 2 * n:
            print('VERIFY_FAIL')
            exit()
    
    # 답 검증
    result = a[1] + a[22]
    if result != 22:
        print('VERIFY_FAIL')
        exit()

print('VERIFY_PASS')