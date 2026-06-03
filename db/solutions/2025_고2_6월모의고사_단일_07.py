import sympy as sp
theta = sp.Symbol('theta', real=True)
sin_theta = sp.sqrt(3)/3
cos_theta = -sp.sqrt(6)/3

# 주어진 조건 확인: cos²θ + sin²θ = 1
identity_check = sp.simplify(cos_theta**2 + sin_theta**2)
assert identity_check == 1, f'Identity failed: {identity_check}'

# 원래 식 확인: (cos²θ/sinθ) + sinθ = √3
lhs = sp.simplify(cos_theta**2 / sin_theta + sin_theta)
rhs = sp.sqrt(3)
assert sp.simplify(lhs - rhs) == 0, f'Equation failed: {lhs} != {rhs}'

print('VERIFY_PASS')