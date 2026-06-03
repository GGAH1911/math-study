from sympy import *

# 원래 문제 조건
AB_len = Integer(5)
AC_len = 3 * sqrt(5)
AD_len = Integer(7)

# BC = CD 조건으로부터 cos(alpha) 유도
# BC^2 = AB^2+AC^2-2*AB*AC*cos(a), CD^2 = AC^2+AD^2-2*AC*AD*cos(a)
# BC^2 = CD^2 => AB^2 - AD^2 = 2*AC*cos(a)*(AB - AD)
# => cos(a) = (AB+AD)/(2*AC)
cos_a = (AB_len + AD_len) / (2 * AC_len)
cos_a = simplify(cos_a)  # 2/sqrt(5)

# BC^2 와 CD^2 검증 (BC = CD 확인)
BC_sq = AB_len**2 + AC_len**2 - 2*AB_len*AC_len*cos_a
CD_sq = AC_len**2 + AD_len**2 - 2*AC_len*AD_len*cos_a
assert simplify(BC_sq - CD_sq) == 0, 'BC != CD'

# BC 길이
BC_len = sqrt(simplify(BC_sq))  # sqrt(10)

# sin(alpha)
sin_a = sqrt(1 - cos_a**2)
sin_a = simplify(sin_a)  # 1/sqrt(5)

# 삼각형 ABC에서 사인법칙으로 반지름 계산: BC/sin(alpha) = 2R
R_val = BC_len / (2 * sin_a)
R_val = simplify(R_val)

R_expected = Rational(5, 2) * sqrt(2)

if simplify(R_val - R_expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: R = {R_val}, expected {R_expected}')
