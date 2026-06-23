from fractions import Fraction
from sympy import symbols, Eq, solve

# 주어진 조건
P_A = Fraction(1, 3)
P_AcB = Fraction(1, 6)  # P(A^c ∩ B)

# A와 B^c가 배반 ⟹ A ∩ B^c = ∅ ⟹ A ⊆ B
# 따라서 A ∩ B = A
P_AB = P_A

# B = (A ∩ B) ∪ (A^c ∩ B) (서로소 분할)
P_B = P_AB + P_AcB
CANDIDATE = P_B

# 검증
print(f'P(A) = {P_A}')
print(f'P(A^c ∩ B) = {P_AcB}')
print(f'P(A ∩ B) = {P_AB} (A ⊆ B이므로)')
print(f'P(B) = {CANDIDATE}')

# 조건 검증
if CANDIDATE == Fraction(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')