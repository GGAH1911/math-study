from fractions import Fraction
import sympy as sp

# 공비와 첫째항 설정
r_squared = Fraction(3, 2)
r_fourth = r_squared ** 2
a = Fraction(5, 1) / r_fourth

# 검증 1: ar^4 = 5
assert a * r_fourth == 5, 'ar^4 should be 5'

# 검증 2: 조건 (가)
a_3 = a * r_squared
a_5 = a * r_fourth
a_7 = a_5 * r_squared
product = a_3 * a_5 * a_7
assert product == 125, f'a_3*a_5*a_7 should be 125, got {product}'

# 검증 3: 조건 (나)
a_4 = a * r_squared * r_squared / r_squared
a_4 = a * (r_squared ** 1.5) if False else a * r_squared * (r_squared ** 0.5)
r_val = sp.sqrt(Fraction(3, 2))
a_4_exact = a * r_val ** 3
a_6_exact = a * r_val ** 5
a_8_exact = a * r_val ** 7
ratio = (a_4_exact + a_8_exact) / a_6_exact
ratio_simplified = sp.simplify(ratio)
assert ratio_simplified == Fraction(13, 6), f'(a_4+a_8)/a_6 should be 13/6'

# a_9 계산
r_eighth = r_squared ** 4
a_9 = a * r_eighth
assert a_9 == Fraction(45, 4), f'a_9 should be 45/4, got {a_9}'
print('VERIFY_PASS')