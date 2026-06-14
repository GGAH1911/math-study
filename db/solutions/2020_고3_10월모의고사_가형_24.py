CANDIDATE = 48
from sympy import *
theta = symbols('theta', real=True)
# 원래 조건: sin(pi/2 + theta)*tan(pi - theta) = 3/5
expr = sin(pi/2 + theta) * tan(pi - theta)
# expr를 단순화
expr_simplified = simplify(expr)  # should be -sin(theta)
# CANDIDATE = 30*(1 - sin_val) => sin_val = 1 - CANDIDATE/30
sin_val = 1 - Rational(CANDIDATE, 30)
# 검산: expr_simplified at sin(theta)=sin_val should equal 3/5
check_val = expr_simplified.subs(sin(theta), sin_val)
check_val = simplify(check_val)
if check_val == Rational(3, 5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', check_val)
