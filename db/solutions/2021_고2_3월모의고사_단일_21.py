from itertools import combinations
chairs = [11,12,13,14,15,16,17,23,24,25]
A_seats = [s for s in chairs if s >= 24]
B_seats = [s for s in chairs if s <= 14]
count = 0
for a in A_seats:
    for b in B_seats:
        if a == b:
            continue
        remaining = [s for s in chairs if s != a and s != b]
        for others in combinations(remaining, 3):
            five = [a, b] + list(others)
            ok = True
            for i in range(5):
                for j in range(i+1, 5):
                    d = abs(five[i] - five[j])
                    if d == 1 or d == 10:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                count += 6  # 3! for the 3 unnamed students
print('VERIFY_PASS' if count == 60 else f'VERIFY_FAIL: got {count}')