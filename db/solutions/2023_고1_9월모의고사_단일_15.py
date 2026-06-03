import sympy as sp
x, m = sp.symbols('x m', real=True)

# 곡선: y = (x-4)^2 + m
# 직선: y = 2x + 3
# 접점에서 교점 방정식
eq = (x - 4)**2 + 12 - (2*x + 3)
eq_simplified = sp.expand(eq)

# 중근 조건: 판별식 = 0
coeffs = sp.Poly(eq_simplified, x).all_coeffs()
if len(coeffs) == 3:
    a, b, c = coeffs
    discriminant = b**2 - 4*a*c
    if discriminant == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')