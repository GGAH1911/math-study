from sympy import binomial, Rational
# 검은 3, 흰 4, 총 7개에서 3개 동시 추출
total = binomial(7,3)
all_white = binomial(4,3)
P_no_black = Rational(all_white, total)
P_at_least_one_black = 1 - P_no_black
expected = Rational(31,35)
print('VERIFY_PASS' if P_at_least_one_black == expected else 'VERIFY_FAIL')