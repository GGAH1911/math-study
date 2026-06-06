count = 0
for a in range(1, 11):
    for b in range(1, 11 - a):
        for c in range(1, 11 - a - b):
            for d in range(1, 11 - a - b - c):
                e = 11 - a - b - c - d
                if e >= 1:
                    if (a + b) % 2 == 0:
                        even_count = sum(1 for x in [a, b, c, d, e] if x % 2 == 0)
                        if even_count >= 2:
                            count += 1
if count == 75:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')