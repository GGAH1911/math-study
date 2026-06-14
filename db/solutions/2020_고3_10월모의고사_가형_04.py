from sympy import Rational, simplify
from fractions import Fraction

# 문제의 원래 조건
P_A = Rational(2, 5)  # P(A) = 2/5
P_B = Rational(1, 6)  # P(B) = 1/6

# A와 B가 독립이므로 P(A ∩ B) = P(A) × P(B)
P_A_intersect_B = P_A * P_B

# P(A ∪ B) = P(A) + P(B) - P(A ∩ B) 공식
P_A_union_B = P_A + P_B - P_A_intersect_B

print(f"P(A) = {P_A}")
print(f"P(B) = {P_B}")
print(f"P(A ∩ B) (독립) = {P_A_intersect_B}")
print(f"P(A ∪ B) = {P_A} + {P_B} - {P_A_intersect_B} = {P_A_union_B}")

# 검증: 문제 조건 만족 여부
verify_conditions = [
    0 <= P_A_union_B <= 1,                    # 확률 범위
    P_A_union_B >= P_A,                       # P(A∪B) ≥ P(A)
    P_A_union_B >= P_B,                       # P(A∪B) ≥ P(B)
    P_A_intersect_B == P_A * P_B,             # 독립 조건
]

if all(verify_conditions):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")