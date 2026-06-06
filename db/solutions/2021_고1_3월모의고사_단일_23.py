from math import gcd

count = 0
for n in range(1, 31):
    if gcd(n, 99) == 1:
        count += 1

if count == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')