count = 0
for a in range(1, 13):
    for b in range(1, 13):
        if abs(a*a - b*b) != 5:
            continue
        # c+d+e = 12 - a - b, each >= 1
        rem = 12 - a - b
        if rem < 3:
            continue
        for c in range(1, rem-1):
            for d in range(1, rem-c):
                e = rem - c - d
                if e >= 1:
                    count += 1
print('VERIFY_PASS' if count == 30 else f'VERIFY_FAIL count={count}')