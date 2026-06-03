from sympy import symbols, sqrt, Rational, simplify

# 주어진 조건
AB, AC, AD = 3, 5, 6

# 각의 이등분선 정리: BE:EC = 3:5이므로 BE = 3k, EC = 5k
# Stewart 정리: AE² + 15k² = 15
# Power of point: EA·ED = EB·EC = 15k²

k_squared = Rational(7, 12)

# AE² = 15 - 15k²
AE_squared = 15 - 15*k_squared
AE = sqrt(AE_squared)

# ED = AD - AE
ED = AD - AE

# Power of point 검증
EA_ED_product = AE * ED
EB_EC_product = 15 * k_squared

# 정답 확인
if simplify(EA_ED_product - EB_EC_product) == 0 and AE == Rational(5,2) and ED == Rational(7,2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')