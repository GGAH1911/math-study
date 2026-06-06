def verify():
    count = 0
    for f1 in range(1, 11):
        if f1 != 1:
            continue
        for f2 in range(f1, 11):
            if f2 > 2:
                continue
            for f3 in range(f2, 11):
                if f3 > 3:
                    continue
                for f4 in range(f3, 11):
                    if f4 > 4:
                        continue
                    for f5 in range(f4, 11):
                        if f5 > 5:
                            continue
                        f6 = f5 + 6
                        if f6 > 10 or f6 < 6:
                            continue
                        for f7 in range(f6, 11):
                            if f7 < 7:
                                continue
                            for f8 in range(f7, 11):
                                if f8 < 8:
                                    continue
                                for f9 in range(f8, 11):
                                    if f9 < 9:
                                        continue
                                    for f10 in range(f9, 11):
                                        if f10 < 10 or f10 > 10:
                                            continue
                                        count += 1
    print('VERIFY_PASS' if count == 100 else f'VERIFY_FAIL: {count}')

verify()