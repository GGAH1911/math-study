from sympy import binomial, Rational, simplify
# 원래 조건: 흰 3, 검은 4, 총 7개에서 4개 동시 추출, 흰2·검은2 확률
total = binomial(7, 4)
favorable = binomial(3, 2) * binomial(4, 2)
prob = Rational(favorable, total)
CANDIDATE = Rational(18, 35)
if simplify(prob - CANDIDATE) == 0 and prob == Rational(18,35):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')