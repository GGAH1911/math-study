import sympy as sp

# 원래 식 계산
result = sp.Rational(4)**(1 - sp.sqrt(3)) * 2**(2*sp.sqrt(3) - 1)
result_simplified = sp.simplify(result)

# 답 검증
if result_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')