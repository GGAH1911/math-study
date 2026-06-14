from fractions import Fraction
from itertools import product

dice_rolls = list(product(range(1,7), range(1,7), range(1,7)))
total = len(dice_rolls)  # 216

counts = {}
for (a, b, c) in dice_rolls:
    s = a + b + c
    counts[s] = counts.get(s, 0) + 1

# E(X) 직접 계산
E_X = Fraction(0)
for k in range(3, 19):
    p_k = Fraction(counts.get(k, 0), total)
    E_X += k * p_k

# (가)=7 검증: P(X=k) == P(X=21-k)
ga_ok = all(counts.get(k,0) == counts.get(21-k,0) for k in range(3,19))

# (나)=21, (다)=1/2
p_val = 7
q_val = 21
r_val = Fraction(1, 2)

result = Fraction(p_val + q_val, 1) / r_val  # (p+q)/r

# E(X) = 21/2 검증
expected_E = Fraction(21, 2)

sum_3_10 = sum(Fraction(counts.get(k,0), total) for k in range(3, 11))

if ga_ok and E_X == expected_E and sum_3_10 == r_val and result == 56:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'E(X)={E_X}, expected={expected_E}, ga_ok={ga_ok}, sum_3_10={sum_3_10}, result={result}')
