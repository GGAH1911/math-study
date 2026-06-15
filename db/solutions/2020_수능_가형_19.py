from sympy import symbols, cos, sin, sqrt, solve, simplify

theta = symbols('theta', real=True)

# C = (4 + 4*cos(theta), 4*sin(theta))
# D = (12 - 8*cos(theta), -8*sin(theta))

# D가 원 (x-4)^2 + y^2 = 16 위에 있어야 함
D_x = 12 - 8*cos(theta)
D_y = -8*sin(theta)

circle_eq = (D_x - 4)**2 + D_y**2 - 16
circle_eq = simplify(circle_eq)

# cos(theta) 구하기
sol_cos = solve(circle_eq, cos(theta))
print(f'cos(theta) = {sol_cos}')

cos_val = sol_cos[0]
print(f'cos(theta) = {cos_val}')

# sin^2(theta) 계산
sin_sq = 1 - cos_val**2
sin_sq = simplify(sin_sq)
print(f'sin^2(theta) = {sin_sq}')

# |AD|^2 계산
AD_sq = (12 - 8*cos_val)**2 + (8**2 * sin_sq)
AD_sq = simplify(AD_sq)
print(f'|AD|^2 = {AD_sq}')

if AD_sq == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')