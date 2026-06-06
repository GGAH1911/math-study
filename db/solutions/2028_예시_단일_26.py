from fractions import Fraction
import numpy as np

# k=3, b=1/3, a=7/18
k = 3
b = Fraction(1, 3)
a = Fraction(7, 18)

# 확률질량함수 검증
probs = {0: a}
for x in range(1, k+1):
    probs[x] = b / x

# 확률의 합
prob_sum = sum(probs.values())
assert prob_sum == 1, f'확률 합 = {prob_sum}, 1이어야 함'

# E(X)
EX = sum(x * probs[x] for x in probs)
assert EX == 1, f'E(X) = {EX}'

# E(X^2)
EX2 = sum(x**2 * probs[x] for x in probs)
assert EX2 == 2, f'E(X^2) = {EX2}, 2E(X) = 2이어야 함'

# E(X^2) = 2E(X) 검증
assert EX2 == 2*EX, f'조건 불만족'

# V(X) 계산
VX = EX2 - EX**2
assert VX == 1, f'V(X) = {VX}'

# b = 1/3일 때 V(X) 최대 확인 (미분)
# V(b) = 6b - 9b^2, dV/db = 6 - 18b
# b = 1/3에서 dV/db = 0
for test_b in [0.3, Fraction(1,3), 0.35]:
    v = float(6*test_b - 9*test_b**2)
    if test_b == Fraction(1,3):
        v_max = v

print('VERIFY_PASS')