from itertools import permutations
from fractions import Fraction
from math import factorial

balls = list(range(1, 10))  # 1..9, distinct
total = factorial(9)

def compute_X(perm):
    # rule derived from the problem's case analysis:
    # first even -> X=1; first odd -> continue until next odd, X = its position
    if perm[0] % 2 == 0:
        return 1
    for i in range(1, len(perm)):
        if perm[i] % 2 == 1:
            return i + 1
    return len(perm)

counts = {}
for perm in permutations(balls):
    x = compute_X(perm)
    counts[x] = counts.get(x, 0) + 1

P = {k: Fraction(c, total) for k, c in counts.items()}

m = max(counts)          # max value of X (가)
a = m
EX = sum(k * P[k] for k in P)

def nPr(n, r):
    return factorial(n) // factorial(n - r)

f4 = P[4] * nPr(9, 4)    # numerator (나) at k=4 = P(X=4)*9P4

answer_value = a + f4

ok = (sum(P.values()) == 1) and (EX == 2) and (f4 == int(f4)) and (m == 6) and (answer_value == 246)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
