count = 0
X = range(1, 7)
for f1 in X:
    for f2 in X:
        for f3 in X:
            for f4 in X:
                for f5 in X:
                    for f6 in X:
                        cond_ga = (2*f1 + 2*f2 + f6 == f3 + 16)
                        cond_na = (f3 <= f4 <= f5 <= f6)
                        if cond_ga and cond_na:
                            count += 1
if count == 324:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')