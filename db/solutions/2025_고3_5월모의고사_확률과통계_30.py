import itertools

count = 0
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            for d in range(1, 7):
                for e in range(1, 7):
                    toggles = [0] * 6
                    for roll in [a, b, c, d, e]:
                        for i in range(roll):
                            toggles[i] += 1
                    all_off = all(t % 2 == 1 for t in toggles)
                    if all_off:
                        count += 1

if count == 376:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')