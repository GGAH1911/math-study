from sympy import *

R2 = Rational(3840, 119)
R = sqrt(R2)

# 확장 사인법칙으로 각 삼각값 계산
sin_alpha = sqrt(30)/R
cos_alpha = sqrt(1 - sin_alpha**2)
sin_tAB = Rational(2)/R
cos_tAB = sqrt(1 - sin_tAB**2)
sin_tCD = Rational(4)/R
cos_tCD = sqrt(1 - sin_tCD**2)

# 검증 1: AB=4, BC=2sqrt(30), CD=8 조건
assert simplify(2*R*sin_tAB - 4) == 0
assert simplify(2*R*sin_alpha - 2*sqrt(30)) == 0
assert simplify(2*R*sin_tCD - 8) == 0

# 검증 2: cos(theta_AB + theta_CD) = 5/12 (즉 cos(alpha+beta) = -5/12)
cos_tAB_tCD = cos_tAB*cos_tCD - sin_tAB*sin_tCD
assert simplify(cos_tAB_tCD - Rational(5,12)) == 0

# sin(beta) 계산: beta = pi - theta_AB - alpha - theta_CD
sin_tAB_alpha = sin_tAB*cos_alpha + cos_tAB*sin_alpha
cos_tAB_alpha = cos_tAB*cos_alpha - sin_tAB*sin_alpha
sin_beta = sin_tAB_alpha*cos_tCD + cos_tAB_alpha*sin_tCD

# sin(alpha+beta) = sqrt(119)/12
sin_a_b = sqrt(Rational(119, 144))

# AE = AB * sin(beta) / sin(alpha+beta)
AE = 4 * sin_beta / sin_a_b

if simplify(AE**2 - 8) == 0:  # 2sqrt(2)이면 AE^2 = 8
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL, AE^2 =', simplify(AE**2))
