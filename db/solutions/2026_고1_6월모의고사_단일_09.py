import sympy as sp
m, x = sp.symbols('m x', real=True)
a, b = 3, -sp.Rational(9, 4)

# 이차함수
f = x**2 - 2*m*x + m**2 + 3*m

# 직선
g = a*x + b

# 교점 방정식
eq = f - g
eq_expanded = sp.expand(eq)

# 판별식 계산
coeffs = sp.Poly(eq_expanded, x).all_coeffs()
A, B, C = coeffs[0], coeffs[1], coeffs[2]

# 판별식
discriminant = B**2 - 4*A*C
discriminant_simplified = sp.simplify(discriminant)

if discriminant_simplified == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: 판별식 = {discriminant_simplified}')