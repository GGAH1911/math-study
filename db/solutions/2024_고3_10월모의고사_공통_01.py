from fractions import Fraction
base_exp = Fraction(5, 3)
outer_exp = Fraction(6, 5)
result_exp = base_exp * outer_exp  # 6/3 = 2
result = 2 ** result_exp
print('VERIFY_PASS' if result == 4 else f'VERIFY_FAIL: got {result}')