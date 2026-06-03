from itertools import product

count = 0
for f1 in [1, 2, 3, 4]:
    for f2 in [1, 2, 3, 4]:
        for f3 in [1, 2, 3, 4]:
            for f4 in [1, 2, 3, 4]:
                f = {1: f1, 2: f2, 3: f3, 4: f4}
                cond_ga = f[1] + f[2] + f[3] >= 3 * f[4]
                cond_na = (f[1] != f[4]) and (f[2] != f[4]) and (f[3] != f[4])
                if cond_ga and cond_na:
                    count += 1

if count == 57:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count} instead of 57')