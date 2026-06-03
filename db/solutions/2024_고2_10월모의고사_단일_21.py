from fractions import Fraction

def next_term(an, a1):
    if an >= 1:
        return Fraction(1, 2) * an
    else:
        return Fraction(1, 2) * (an + a1)

def compute(k):
    a1 = Fraction(k)
    a = [a1]
    for _ in range(5):
        a.append(next_term(a[-1], a1))
    return a[4] + 2 * a[5]

candidates = [Fraction(16, 1), Fraction(16, 5)]
valid = [k for k in candidates if compute(k) == 2]
total = sum(valid)
if total == Fraction(96, 5) and len(valid) == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')