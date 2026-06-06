from fractions import Fraction

def a_next(a_n):
    if a_n > 0:
        return Fraction(1, 1) / a_n - 1
    else:
        return -a_n

a1 = Fraction(25, 4)
seq = [a1]
for i in range(14):
    seq.append(a_next(seq[-1]))

a14 = seq[13]
a15 = seq[14]
result = 12 * (a14 + a15)

if result == 28:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')