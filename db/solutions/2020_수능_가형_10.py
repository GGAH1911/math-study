from sympy import Rational, simplify

# 주어진 조건과 우리의 답
tan_alpha = Rational(12, 5)
tan_beta = Rational(3, 2)

# 검증 1: tan(α + β) = -3/2 조건 확인
tan_alpha_plus_beta = (tan_alpha + tan_beta) / (1 - tan_alpha * tan_beta)
tan_alpha_plus_beta = simplify(tan_alpha_plus_beta)

if tan_alpha_plus_beta != Rational(-3, 2):
    print('VERIFY_FAIL')
    exit()

# 검증 2: α = 180° - 2β 조건 확인
# tan(2β) = 2tan(β) / (1 - tan²(β))
tan_2beta = (2 * tan_beta) / (1 - tan_beta**2)
tan_2beta = simplify(tan_2beta)

# tan(α) = tan(180° - 2β) = -tan(2β)
tan_alpha_from_condition = -tan_2beta
tan_alpha_from_condition = simplify(tan_alpha_from_condition)

# 우리의 답이 맞는지 확인
if tan_alpha_from_condition != tan_alpha:
    print('VERIFY_FAIL')
    exit()

print('VERIFY_PASS')