from fractions import Fraction
from math import comb

p = Fraction(1, 3)
q = Fraction(2, 3)

def prob(k):
    return Fraction(comb(5, k)) * p**k * q**(5-k)

# B odd: k even; A+C >= 8: k <= 2
numerator = prob(0) + prob(2)        # k in {0,2}
denominator = prob(0) + prob(2) + prob(4)  # k in {0,2,4}

result = numerator / denominator
expected = Fraction(56, 61)

print('numerator:', numerator, '=', float(numerator))
print('denominator:', denominator, '=', float(denominator))
print('result:', result, '=', float(result))
print('expected:', expected)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
