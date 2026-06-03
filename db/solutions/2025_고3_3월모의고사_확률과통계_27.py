def verify():
    X = {1, 2, 3, 4, 5, 6}
    count = 0
    
    for f1 in range(1, 4):
        for f2 in range(f1, 4):
            for f4 in range(3, 7):
                for f5 in range(f4, 7):
                    f = {1: f1, 2: f2, 3: 3, 4: f4, 5: f5, 6: 6}
                    
                    cond_ga = all(f[x] <= f[x+1] for x in range(1, 6))
                    cond_na = f[f[3]] == 3 and f[f[6]] == 6
                    
                    if cond_ga and cond_na:
                        count += 1
    
    print('VERIFY_PASS' if count == 60 else f'VERIFY_FAIL: got {count}')

verify()