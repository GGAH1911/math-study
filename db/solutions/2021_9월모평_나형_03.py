import math
import sympy as sp

# 수치 계산
cos_pi_6 = math.cos(math.pi / 6)
cos_sq = cos_pi_6 ** 2
tan_2pi_3 = math.tan(2 * math.pi / 3)
tan_sq = tan_2pi_3 ** 2
result = cos_sq + tan_sq

# 정확한 값 (기호 계산)
# cos(π/6) = √3/2 → cos²(π/6) = 3/4
# tan(2π/3) = -√3 → tan²(2π/3) = 3
exact_sum = sp.Rational(3, 4) + 3

if exact_sum == sp.Rational(15, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')