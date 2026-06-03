import sympy as sp

# 주어진 조건
AB = 4
CA = 8
# 각도 A = 120도
A_deg = 120
A_rad = sp.pi * A_deg / 180

# 코사인 법칙으로 a = BC 계산
a = sp.sqrt(AB**2 + CA**2 - 2*AB*CA*sp.cos(A_rad))
# a = 4*sqrt(7)

# 2R 계산
two_R = a / sp.sin(A_rad)

# 조건 검증: a(sinB + sinC) = 6*sqrt(3)
sinB = CA / two_R
sinC = AB / two_R
check1 = sp.simplify(a * (sinB + sinC) - 6*sp.sqrt(3))

# AP 계산: 각의 이등분선 공식
AP = 2 * AB * CA * sp.cos(A_rad / 2) / (AB + CA)
AP_simplified = sp.simplify(AP)

# 답이 8/3인지 확인
check2 = sp.simplify(AP_simplified - sp.Rational(8, 3))

# 스튜어트 정리로도 검증
BP = a * sp.Rational(1, 3)
PC = a * sp.Rational(2, 3)
# b^2*m + c^2*n = a*(d^2 + m*n)
stewart_lhs = CA**2 * BP + AB**2 * PC
stewart_rhs_no_d = a * BP * PC
AP2_from_stewart = (stewart_lhs - stewart_rhs_no_d) / a
check3 = sp.simplify(AP2_from_stewart - sp.Rational(64, 9))

if check1 == 0 and check2 == 0 and check3 == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: check1={check1}, check2={check2}, check3={check3}')
