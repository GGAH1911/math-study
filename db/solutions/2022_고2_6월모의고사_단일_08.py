from sympy import *
cos_theta = Rational(-2, 3)
sin_theta = sqrt(5) / 3

# 원래 조건 검증: sin²θ + cos²θ = 1
result = sin_theta**2 + cos_theta**2
if simplify(result) == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')