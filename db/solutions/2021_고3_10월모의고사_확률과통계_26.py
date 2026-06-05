from math import gcd

count = 0
for a in range(1, 7):
    for b in range(1, 7):
        if gcd(a, b) % 2 == 1:
            count += 1

probability = count / 36
expected = 3 / 4

if abs(probability - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')