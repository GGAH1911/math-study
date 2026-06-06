from fractions import Fraction
from itertools import product

# 모든 경우의 확률 계산
prob_1, prob_2 = Fraction(1, 3), Fraction(2, 3)
count_target = Fraction(0)  # a1=a4=1 and S1>S2
count_condition = Fraction(0)  # S1>S2

for outcome in product([1, 2], repeat=6):
    a1, a2, a3, a4, a5, a6 = outcome
    prob = (prob_1 if a == 1 else prob_2 for a in outcome)
    prob = Fraction(1)
    for a in outcome:
        prob *= (prob_1 if a == 1 else prob_2)
    
    s1, s2 = a1 + a2 + a3, a4 + a5 + a6
    
    if s1 > s2:
        count_condition += prob
        if a1 == 1 and a4 == 1:
            count_target += prob

conditional = count_target / count_condition
assert conditional == Fraction(12, 121), f"Expected 12/121, got {conditional}"
assert conditional.numerator + conditional.denominator == 133
print('VERIFY_PASS')