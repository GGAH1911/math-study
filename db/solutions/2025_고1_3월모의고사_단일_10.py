def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

count = 0
total = 0
for die1 in range(1, 7):
    for die2 in range(1, 7):
        total += 1
        s = die1 + die2
        if is_prime(s):
            count += 1

from fractions import Fraction
prob = Fraction(count, total)
if prob == Fraction(5, 12):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')