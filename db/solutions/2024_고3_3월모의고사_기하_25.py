import sympy as sp

a = sp.Integer(12)
b = sp.Rational(3, 4) * a  # b = 9
c = sp.sqrt(a**2 + b**2)

# 검증 1: 두 초점 사이 거리 = 30
assert 2*c == 30, f'초점 거리 오류: {2*c}'

# 검증 2: 점근선 기울기 = 3/4
slope = b / a
assert slope == sp.Rational(3, 4), f'점근선 기울기 오류: {slope}'

# 검증 3: 주축의 길이 = 24
transverse_axis = 2 * a
assert transverse_axis == 24, f'주축 길이 오류: {transverse_axis}'

print('VERIFY_PASS')
