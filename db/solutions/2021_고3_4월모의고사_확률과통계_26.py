from itertools import product

count = 0
for a1, a2, a3, a4, a5 in product(range(1, 6), repeat=5):
    N = 10000*a1 + 1000*a2 + 100*a3 + 10*a4 + a5
    if (10000 < N < 30000) and (N % 2 == 1):
        count += 1

if count == 750:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')