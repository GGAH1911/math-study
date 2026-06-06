from sympy import sqrt, simplify

CANDIDATE = 5

# 원래 문제의 식: (5^(2-√3))^(2+√3)
# 지수법칙 적용: 5^((2-√3)(2+√3))

# 지수 부분 계산
exponent_factor_1 = 2 - sqrt(3)
exponent_factor_2 = 2 + sqrt(3)
exponent = simplify(exponent_factor_1 * exponent_factor_2)

# 원래 식 계산
original_expression_result = simplify(5 ** exponent)

# 정답 검증
if original_expression_result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")