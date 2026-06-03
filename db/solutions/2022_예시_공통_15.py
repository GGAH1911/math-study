def verify():
    # 각 경로의 첫 5개 항 정의
    paths = [
        [29, 23, 17, 11, 5],
        [-10, 23, 17, 11, 5],
        [8, 2, -4, 11, 5],
        [17, 11, 5, -1, 5],
        [-4, 11, 5, -1, 5],
        [5, -1, 5, -1, 5]
    ]
    
    def f(a_n):
        if a_n >= 0:
            return a_n - 6
        else:
            return -2 * a_n + 3
    
    # 모든 경로가 점화식을 만족하는지 확인
    for path in paths:
        for i in range(len(path) - 1):
            if f(path[i]) != path[i+1]:
                print('VERIFY_FAIL')
                return
    
    # 각 경로의 합 계산
    sums = []
    for path in paths:
        # 경로의 처음 4항만 합산
        s = sum(path[:4])
        # n >= 5부터의 합 추가: 48개의 5와 48개의 -1
        s += 48 * 5 + 48 * (-1)  # = 48 * 4 = 192
        sums.append(s)
    
    M = max(sums)  # 272
    m = min(sums)  # 200
    
    if M - m == 72:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()