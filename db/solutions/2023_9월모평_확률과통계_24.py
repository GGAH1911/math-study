import sympy as sp

# 주어진 조건
# P(A∪B) = 1
# P(A∩B) = 1/4
# P(A|B) = P(B|A)

P_A = sp.Rational(5, 8)
P_B = sp.Rational(5, 8)
P_AandB = sp.Rational(1, 4)

# 검증 1: P(A∪B) = P(A) + P(B) - P(A∩B) = 1
P_AorB = P_A + P_B - P_AandB
assert P_AorB == 1, f"P(A∪B) = {P_AorB}, expected 1"

# 검증 2: P(A∩B) = 1/4
assert P_AandB == sp.Rational(1, 4), f"P(A∩B) = {P_AandB}, expected 1/4"

# 검증 3: P(A|B) = P(B|A)
P_A_given_B = P_AandB / P_B
P_B_given_A = P_AandB / P_A
assert P_A_given_B == P_B_given_A, f"P(A|B) = {P_A_given_B}, P(B|A) = {P_B_given_A}"

# 모든 확률이 [0,1] 범위 내
assert 0 <= P_A <= 1, f"P(A) = {P_A} out of range"
assert 0 <= P_B <= 1, f"P(B) = {P_B} out of range"
assert 0 <= P_AandB <= 1, f"P(A∩B) = {P_AandB} out of range"

print('VERIFY_PASS')