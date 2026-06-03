from fractions import Fraction

# Given conditions
P_A = Fraction(1, 3)  # derived
P_B = Fraction(3, 4)  # answer to verify

# Check condition 1: P(A^C) = 2*P(A)
P_AC = 1 - P_A
if P_AC == 2 * P_A:
    check1 = True
else:
    check1 = False

# Check condition 2: P(A ∩ B) = 1/4 (independence)
P_A_intersect_B = P_A * P_B  # independent
if P_A_intersect_B == Fraction(1, 4):
    check2 = True
else:
    check2 = False

if check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')