from sympy import symbols, Rational, solve

# 조건: P(A^C) = 2*P(A)
PA = Rational(1, 3)  # P(A) = 1/3
PA_complement = 2 * PA  # P(A^C) = 2/3

# 검증: P(A^C) = 1 - P(A)
assert 1 - PA == PA_complement, 'P(A^C) 조건 불만족'

# A, B 배반사건이고 P(A ∪ B) = 1
PB = 1 - PA  # P(B) = 1 - P(A) = 2/3

# 검증: P(A ∪ B) = P(A) + P(B) (배반사건)
P_union = PA + PB
assert P_union == 1, 'P(A ∪ B) = 1 조건 불만족'

print('VERIFY_PASS')