import sympy as sp

theta = sp.Symbol('theta', real=True)

sin_val = sp.sqrt(2) / 10
cos_val = -7*sp.sqrt(2) / 10

# 조건 1: cos(theta) < 0
assert cos_val < 0, 'cos 부호 실패'

# 조건 2: sin(-theta) = (1/7)*cos(theta)
lhs = -sin_val  # sin(-theta) = -sin(theta)
rhs = sp.Rational(1, 7) * cos_val
assert sp.simplify(lhs - rhs) == 0, 'sin(-theta) 조건 실패'

# 피타고라스 항등식
assert sp.simplify(sin_val**2 + cos_val**2 - 1) == 0, '항등식 실패'

print('VERIFY_PASS')
