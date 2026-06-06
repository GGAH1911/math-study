def verify_answer():
    count = 0
    # 모든 함수 f: X -> X 탐색
    for f1 in range(1, 6):
        for f2 in range(1, 6):
            for f3 in range(1, 6):
                for f4 in range(1, 6):
                    for f5 in range(1, 6):
                        f = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5}
                        
                        # 조건 (가) 확인
                        if not (f[1] <= f[2] <= f[3]):
                            continue
                        
                        # 조건 (나) 확인
                        if not (1 < f[5] < f[4]):
                            continue
                        
                        # 조건 (다) 확인: f(a)=b, f(b)=a인 서로 다른 a,b 존재
                        found_swap = False
                        for a in range(1, 6):
                            for b in range(1, 6):
                                if a != b and f[a] == b and f[b] == a:
                                    found_swap = True
                                    break
                            if found_swap:
                                break
                        
                        if found_swap:
                            count += 1
    
    if count == 90:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {count}, expected 90')

verify_answer()