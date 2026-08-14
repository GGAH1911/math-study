from sympy import Rational

PA = Rational(2, 3)
PB = Rational(3, 4)

# 독립사건 정의: P(A∩B) = P(A)*P(B)
PA_and_B = PA * PB

expected = Rational(1, 2)

if PA_and_B == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
