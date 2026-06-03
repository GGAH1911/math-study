from sympy import sqrt, simplify

# 주어진 값
AB = 3
BC = 6
sin_theta = 2 * sqrt(14) / 9
AC = 5

# cos θ 계산
cos_theta_squared = 1 - sin_theta**2
cos_theta = sqrt(cos_theta_squared)

# 코사인 법칙으로 검증
AC_calc_squared = AB**2 + BC**2 - 2*AB*BC*cos_theta
AC_calc = sqrt(AC_calc_squared)

# AC = 5가 맞는지 확인
if simplify(AC_calc - AC) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')