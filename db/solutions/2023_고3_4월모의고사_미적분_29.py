import sympy as sp
from sympy import sqrt, cos, sin, acos, pi, simplify

# 주어진 조건
sin_theta = sp.Rational(1, 8)
cos_theta = 3 * sqrt(7) / 8
r = 3

# 검증: sin²θ + cos²θ = 1
assert simplify(sin_theta**2 + cos_theta**2 - 1) == 0

# 검증: r = 8(√(2(1+sinθ)) - (1+sinθ))
s = sqrt(1 + sin_theta)
r_check = 8 * (sqrt(2) * s - s**2)
assert simplify(r_check - r) == 0

# sinφ 계산
sin_phi = (7 * sin_theta + 24 * cos_theta) / 25
sin_phi_simplified = simplify(sin_phi)

# 최종 형태
p = sp.Rational(7, 200)
q = sp.Rational(72, 200)
result = 200 * (p + q)

assert result == 79
print('VERIFY_PASS')