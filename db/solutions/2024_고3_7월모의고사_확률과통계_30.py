count = 0
X = {1, 2, 3, 4}
Y = {1, 2, 3, 4, 5, 6}

for f1 in Y:
    for f2 in Y:
        for f3 in Y:
            for f4 in Y:
                # 조건 (가)
                cond_ga = (f1 <= f2) and (f2 <= f1 + f3) and (f1 + f3 <= f1 + f4)
                # 조건 (나)
                cond_na = (f1 + f2) % 2 == 0
                
                if cond_ga and cond_na:
                    count += 1

if count == 198:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count} instead of 198')