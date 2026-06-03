from sympy import Rational

n = 30
p = Rational(1, 5)
EX = n * p

if EX == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')