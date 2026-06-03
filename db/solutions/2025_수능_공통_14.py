import sympy as sp

t = sp.sqrt(3)
a = 8*t  # BC
b = 7*t  # AC
c = 5*t  # AB

# cos A, sin A
cos_A = (b**2 + c**2 - a**2) / (2*b*c)
sin_A = sp.sqrt(1 - cos_A**2)

# 외접원 반지름
R = sp.simplify(a / (2*sin_A))
assert R == 7, f'R={R} != 7'

# sin A : sin C = 8:5 확인
sin_C = c / (2*R)
ratio = sp.simplify(sin_A / sin_C)
assert ratio == sp.Rational(8,5), f'ratio={ratio}'

# 넓이비 9:35 확인
AD = sp.Rational(3,5)*c
AE = AD
area_ADE = sp.Rational(1,2)*AD*AE*sin_A
area_ABC = sp.Rational(1,2)*b*c*sin_A
ratio_area = sp.simplify(area_ADE/area_ABC)
assert ratio_area == sp.Rational(9,35), f'area ratio={ratio_area}'

# 원 O 반지름
r = AD

# A에서 BC까지 높이
h_A = sp.simplify(2*area_ABC / a)

# 최대 넓이
max_area = sp.simplify(sp.Rational(1,2)*a*(h_A + r))
expected = 36 + 30*sp.sqrt(3)

if sp.simplify(max_area - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {max_area}, expected {expected}')
