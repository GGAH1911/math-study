from sympy import *

k = 256

# a = k^(1/3)
a = k**(Rational(1,3))

# a의 네제곱근 중 양수인 것
fourth_root_a = a**(Rational(1,4))

# 이것이 4^(1/3)과 같아야 한다
target = 4**(Rational(1,3))

# 검증
if simplify(fourth_root_a - target) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')