from fractions import Fraction

P_A = Fraction(2, 3)
P_AuB = Fraction(7, 9)

# 독립: P(A∪B) = P(A) + P(B) - P(A)*P(B)
# 7/9 = 2/3 + P(B) - (2/3)*P(B)
# 7/9 - 2/3 = P(B)*(1 - 2/3)
diff = P_AuB - P_A
coeff = 1 - P_A
P_B = diff / coeff

# 검산
P_AiB = P_A * P_B  # 독립
P_AuB_check = P_A + P_B - P_AiB

CANDIDATE = Fraction(1, 3)
if P_B == CANDIDATE and P_AuB_check == P_AuB:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'P_B={P_B}, P(A∪B)_check={P_AuB_check}')
