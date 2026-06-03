from itertools import product

count = 0
for d in range(100):
    abs_term = abs(d - 1)
    if abs_term > 4:
        break
    target = 4 - abs_term
    for a in range(target + 1):
        for b in range(target + 1 - a):
            for c in range(target + 1 - a - b):
                if a + b + c == target:
                    count += 1

if count == 45:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')