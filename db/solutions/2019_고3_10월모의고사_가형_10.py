from sympy import binomial, Rational, nsimplify
# 주사위 눈 k (1~6), 각 확률 1/6; 동전 6개 앞면 수 X~B(6,1/2)
P = sum(Rational(1,6) * binomial(6,k)*Rational(1,2)**6 for k in range(1,7))
P = P  # exact rational
CANDIDATE = Rational(21,128)
if P == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', P)
