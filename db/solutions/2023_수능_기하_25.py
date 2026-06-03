import sympy as sp

a2, b2 = 8, 2

# 1. 점 (2,1)이 타원 위에 있는지 확인
check_point = sp.Rational(4, a2) + sp.Rational(1, b2)
assert check_point == 1, f'점 검사 실패: {check_point}'

# 2. 접선 기울기 확인: 타원 위 (x0,y0)에서 접선 기울기 = -(b2/a2)*(x0/y0)
x0, y0 = 2, 1
slope = -(sp.Rational(b2, a2)) * sp.Rational(x0, y0)
assert slope == sp.Rational(-1, 2), f'기울기 검사 실패: {slope}'

# 3. 두 초점 거리 계산
c2 = a2 - b2  # = 6
c = sp.sqrt(c2)
distance = 2 * c  # = 2*sqrt(6)

expected = 2 * sp.sqrt(6)
assert sp.simplify(distance - expected) == 0, f'거리 검사 실패: {distance}'

print('VERIFY_PASS')
