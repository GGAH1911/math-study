from fractions import Fraction

p = Fraction(1, 6)
q = Fraction(5, 6)

# C's remaining 2 throws: X ~ Binomial(2, 1/6)
P_X0 = q**2        # c = 1+0 = 1
P_X1 = 2 * p * q   # c = 1+1 = 2
P_X2 = p**2        # c = 1+2 = 3

# A=2, B=1, C=c
# c=1: B·C same → A wins (rule 나) → A or C: YES
# c=2: A·C same → B wins (rule 나) → A or C: NO
# c=3: all diff → C wins (rule 가, most 1s) → A or C: YES
P_AorC = P_X0 * 1 + P_X1 * 0 + P_X2 * 1

CANDIDATE = Fraction(13, 18)

if P_AorC == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed={P_AorC}, candidate={CANDIDATE}')
