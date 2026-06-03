from math import gcd

count_coprime = 0
total = 0

for a in range(1, 7):
    for b in [7, 8, 9]:
        total += 1
        if gcd(a, b) == 1:
            count_coprime += 1

prob = count_coprime / total
expected = 13/18

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')