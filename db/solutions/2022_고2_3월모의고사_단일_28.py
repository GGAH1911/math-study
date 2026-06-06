def verify():
    count = 0
    # T는 정삼각형의 수, L, M, R은 정사각형의 수
    for T in range(1, 7):
        for L in range(1, 7):
            for M in range(1, 7):
                for R in range(1, 7):
                    # 조건 (가): 세 정사각형의 수가 정삼각형의 수보다 작아야 함
                    if L < T and M < T and R < T:
                        # 조건 (나): 변을 공유하는 정사각형들이 달라야 함
                        if L != M and M != R:
                            count += 1
    if count == 130:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: {count}')
verify()