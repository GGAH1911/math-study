import sympy as sp
from sympy import sqrt, symbols, solve, simplify

# 기본 설정
x0 = 9*sqrt(17)/17
y0 = 32*sqrt(17)/17

# 쌍곡선 방정식 확인
hyperbola = x0**2 - y0**2/16 - 1
verify_hyperbola = simplify(hyperbola)

# 주어진 조건식 확인: 17y0^2 - 24*sqrt(17)*y0 - 256 = 0
condition = 17*y0**2 - 24*sqrt(17)*y0 - 256
verify_condition = simplify(condition)

# 초점까지 거리
PF_squared = (x0 - sqrt(17))**2 + y0**2
PF = sqrt(simplify(PF_squared))

PF_prime_squared = (x0 + sqrt(17))**2 + y0**2
PF_prime = sqrt(simplify(PF_prime_squared))

# 쌍곡선 초점성질
focal_property = PF_prime - PF
verify_focal = simplify(focal_property)

# 삼각형 넓이
area = sp.Rational(1,2) * 2*sqrt(17) * y0
area_simplified = simplify(area)

# 최종 검증
if verify_hyperbola == 0 and verify_condition == 0 and verify_focal == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')