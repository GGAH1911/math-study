from fractions import Fraction

count = 0
for k in range(1, 15):
    r1 = Fraction(k**2 + 9, 10*k)
    r2 = Fraction(3, k)
    converges = False
    if r1 < 1 and r2 < 1:
        converges = True
    elif r1 < 1 and r2 == 1:
        converges = True
    elif r1 == 1 and r2 < 1:
        converges = True
    if converges:
        count += 1

if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')