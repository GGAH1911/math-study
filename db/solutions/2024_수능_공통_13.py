import sympy as sp
from sympy import sqrt, Rational, pi, sin, cos, simplify

# 주어진 조건
AB = 3
BC = sqrt(13)
angle_BAC = pi / 3

# AC 계산 (코사인 법칙)
AC_val = 4  # 검증: (4-4)(4+1) = 0
BC_check = sqrt(9 + 16 - 2*3*4*cos(pi/3))
assert simplify(BC_check - sqrt(13)) == 0, 'AC 검증 실패'

# S1 계산
S1 = Rational(1,2) * 3 * 4 * sin(pi/3)
S1_val = simplify(S1)
assert S1_val == 3*sqrt(3), 'S1 검증 실패'

# S2 계산
S2 = Rational(5,6) * S1_val
S2_val = simplify(S2)
assert S2_val == Rational(5,2)*sqrt(3), 'S2 검증 실패'

# sin(angle_ADC) 계산
AD_CD_product = 9
sin_ADC = 2 * S2_val / AD_CD_product
sin_ADC = simplify(sin_ADC)
assert sin_ADC == Rational(5,9)*sqrt(3), 'sin(angle_ADC) 검증 실패'

# 정현법칙: AC/sin(angle_ADC) = 2R
R_over_sin_ADC = AC_val / (2 * sin_ADC**2)
result = simplify(R_over_sin_ADC)
assert result == Rational(54, 25), f'최종 답 검증 실패: {result}'
print('VERIFY_PASS')