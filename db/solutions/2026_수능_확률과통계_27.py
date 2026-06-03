from fractions import Fraction

# 확률 분포 (원래 문제 조건 그대로)
probs = {}
for x in range(4):
    probs[x] = Fraction(abs(2*x - 1), 12)
# a 결정
total = sum(probs.values())
a = 1 - total  # = 2/12 = 1/6
probs[4] = a

assert sum(probs.values()) == 1, 'probabilities do not sum to 1'
assert a != 0, 'a must be non-zero'

# E(X), E(X^2)
EX  = sum(Fraction(x) * p for x, p in probs.items())
EX2 = sum(Fraction(x*x) * p for x, p in probs.items())
VX  = EX2 - EX**2

# V(1/a * X) = (1/a)^2 * V(X)
coeff = Fraction(1, 1) / a   # = 6
result = coeff**2 * VX

if result == 45:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')
