import sympy as sp
from sympy import sqrt, sin, cos, asin, acos, atan, simplify

# theta_E 설정
theta_E = 2 * atan(sp.Rational(1,2))
sin_theta_E = sin(theta_E)
cos_theta_E = cos(theta_E)

# 검증: sin(theta_E) = 4/5, cos(theta_E) = 3/5
sin_E_simplified = simplify(sin_theta_E)
cos_E_simplified = simplify(cos_theta_E)

print(f'sin(theta_E) = {sin_E_simplified}')
print(f'cos(theta_E) = {cos_E_simplified}')

# E, B, O 좌표
E = (cos_E_simplified, sin_E_simplified)
B = (1, 0)
O = (0, 0)

# 벡터 BO, BE
BO = (O[0] - B[0], O[1] - B[1])
BE = (E[0] - B[0], E[1] - B[1])

# 내적
dot_product = BO[0] * BE[0] + BO[1] * BE[1]

# 크기
mag_BO = sqrt(BO[0]**2 + BO[1]**2)
mag_BE = sqrt(BE[0]**2 + BE[1]**2)

# cos(angle OBE)
cos_OBE = simplify(dot_product / (mag_BO * mag_BE))

print(f'cos(∠OBE) = {cos_OBE}')

if simplify(cos_OBE - sqrt(5)/5) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')