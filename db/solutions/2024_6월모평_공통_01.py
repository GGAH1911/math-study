import sympy as sp

# 원래 문제의 식
result = sp.cbrt(27) * (4 ** (-sp.Rational(1,2)))
result_simplified = sp.simplify(result)

# 답 확인
answer = sp.Rational(3, 2)

if result_simplified == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')