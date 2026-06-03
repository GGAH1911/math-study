import math

count = 0
for a in range(1, 100):
    for b in range(1, 1000):
        cond_ga = 0 < math.log10(b) - math.log10(a) < 1
        cond_na = 2*a + math.log10(b) < 9
        if cond_ga and cond_na:
            count += 1

if count == 56:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')