from sympy import sqrt, simplify, Rational, Pow

CANDIDATE = 4

# 원문제: 2^(1/2) × 8^(1/2)
# 직접 계산
result = sqrt(2) * sqrt(8)
result_simplified = simplify(result)

# 지수법칙으로도 확인: 2^(1/2) × 2^(3/2) = 2^2
result_exp = Pow(2, Rational(1, 2)) * Pow(2, Rational(3, 2))
result_exp_simplified = simplify(result_exp)

if result_simplified == CANDIDATE and result_exp_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')