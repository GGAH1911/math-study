from itertools import product
from fractions import Fraction

P = {}
for a, b, c in product(range(1, 7), repeat=3):
    X = a + b + c
    P[X] = P.get(X, 0) + 1

total = 6**3
for k in P:
    P[k] = Fraction(P[k], total)

E_X = sum(Fraction(k) * P[k] for k in P)
sum_prob = sum(P.get(k, 0) for k in range(3, 11))

if E_X == 21 * sum_prob and sum_prob == Fraction(1, 2):
    p, q, r = 7, 21, Fraction(1, 2)
    result = (p + q) / r
    if result == 56:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')