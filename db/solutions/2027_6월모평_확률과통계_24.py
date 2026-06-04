from fractions import Fraction

# 주어진 조건
P_A_and_B = Fraction(1, 3)
P_A_and_Bc = Fraction(3, 8)

# P(A) = P(A ∩ B) + P(A ∩ B^C)
P_A = P_A_and_B + P_A_and_Bc
print(f'P(A) = {P_A}')

# P(A^C) = 1 - P(A)
P_Ac = 1 - P_A
print(f'P(A^C) = {P_Ac}')

# 검증: 계산된 값이 7/24인지 확인
expected = Fraction(7, 24)
if P_Ac == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')