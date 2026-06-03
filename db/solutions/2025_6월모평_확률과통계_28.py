from fractions import Fraction

P = {0: Fraction(0), 1: Fraction(0), 2: Fraction(0), 3: Fraction(1), 4: Fraction(0)}

for _ in range(5):
    new_P = {k: Fraction(0) for k in range(5)}
    for k in range(5):
        if P[k] == 0:
            continue
        if k > 0:
            new_P[k-1] += P[k] * Fraction(k, 4)
        if k < 4:
            new_P[k+1] += P[k] * Fraction(4-k, 4)
    P = new_P

p_all_heads = P[4]   # 17/128
p_all_tails = P[0]   # 15/128
p_same = p_all_heads + p_all_tails  # 32/128 = 1/4
cond = p_all_heads / p_same          # 17/32

if cond == Fraction(17, 32):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')