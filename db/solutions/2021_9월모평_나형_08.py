from fractions import Fraction
a_values = [1, 3, 5, 7]
b_values = [4, 6, 8, 10]
count = 0
for a in a_values:
    for b in b_values:
        ratio = Fraction(b, a)
        if 1 < ratio < 4:
            count += 1
prob = Fraction(count, 16)
expected = Fraction(9, 16)
if prob == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')