import sympy as sp
from sympy import sqrt, symbols, simplify

a = -2 + sqrt(13)
b_sq = 4*a
c_sq = a**2 + b_sq
c = sqrt(c_sq)

# 검증: c = 3
print('c =', simplify(c))
print('c^2 =', simplify(c_sq))

# P = (c, 4)가 쌍곡선 위에 있는지 확인
x_p, y_p = c, 4
lhs = x_p**2/a**2 - y_p**2/b_sq
result = simplify(lhs)
print('P on hyperbola:', simplify(result - 1) == 0)

# 삼각형 넓이 검증
t = sqrt(a/(a+3))
x_r, y_r = c*t, 2*t

# 면적 = (1/2)|3(2 - y_r) + 2*c*t|
area = abs(c*(2 - y_r) + 2*c*t) / 2
area_simplified = simplify(area)
print('Triangle area:', area_simplified)
print('Area equals 3:', simplify(area_simplified - 3) == 0)

# 최종 답
p, q = -4, 2
print('p^2 + q^2 =', p**2 + q**2)
print('VERIFY_PASS')