from sympy import sqrt, simplify, Rational as R

# 3^(3/2) × √3 계산
result = (3 ** R(3, 2)) * sqrt(3)
result_simplified = simplify(result)

if result_simplified == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')