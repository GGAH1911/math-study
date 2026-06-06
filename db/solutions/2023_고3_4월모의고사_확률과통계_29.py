from itertools import product

count = 0

for f1 in range(1, 6):
    for f2 in range(1, 6):
        for f3 in range(1, 6):
            f4 = f1 + f2 + f3
            if f4 < 1 or f4 > 5:
                continue
            
            for f5 in range(1, 6):
                for f6 in range(1, 6):
                    for f7 in range(1, 6):
                        for f8 in range(1, 6):
                            cond_ga = (f4 == f1 + f2 + f3)
                            cond_na = (2 * f4 == f5 + f6 + f7 + f8)
                            
                            if cond_ga and cond_na:
                                count += 1

if count == 523:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: 523, Got: {count}')