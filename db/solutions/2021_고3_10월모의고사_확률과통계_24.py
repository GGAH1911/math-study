from fractions import Fraction
PA = Fraction(1, 3)
PAc = 1 - PA
assert PAc == Fraction(2, 3)
PB = Fraction(1, 6) / PAc
assert PB == Fraction(1, 4)
verify_condition = PAc * PB
assert verify_condition == Fraction(1, 6), f'Expected 1/6, got {verify_condition}'
PA_union_B = PA + PB
assert PA_union_B == Fraction(7, 12), f'Expected 7/12, got {PA_union_B}'
print('VERIFY_PASS')