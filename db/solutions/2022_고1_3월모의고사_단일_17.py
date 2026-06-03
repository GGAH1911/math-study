from fractions import Fraction
count = 0
for a in range(1, 7):
    for b in range(1, 7):
        value = (a**2) * (3**b) * 5
        divisor = (2**2) * (3**5)
        if value % divisor == 0:
            count += 1
prob = Fraction(count, 36)
expected = Fraction(2, 9)
print('VERIFY_PASS' if prob == expected else 'VERIFY_FAIL')
