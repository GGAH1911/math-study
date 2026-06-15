from sympy import Rational, simplify

# tan(α) = -1/3일 때, tan(π/4 + α) = 1/2인지 검증
tan_alpha = Rational(-1, 3)
tan_pi_4_plus_alpha = (1 + tan_alpha) / (1 - tan_alpha)
tan_pi_4_plus_alpha = simplify(tan_pi_4_plus_alpha)

# 조건: tan(π/4 + α) = 1/2이면 f'(π/4) = 0이 성립
if tan_pi_4_plus_alpha == Rational(1, 2):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")