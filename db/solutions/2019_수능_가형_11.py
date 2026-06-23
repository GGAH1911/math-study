import sympy as sp
from sympy import sin, cos, pi, solve, symbols

theta = symbols('theta', real=True)

# 판별식 조건: D <= 0
D = 16*cos(theta)**2 - 24*sin(theta)

# 부등식을 sin(theta)에 대해 정리
s = sp.Symbol('s')
inequality = 16*(1-s**2) - 24*s

# 16 - 16s^2 - 24s <= 0
# 2s^2 + 3s - 2 >= 0
quad = 2*s**2 + 3*s - 2
roots = solve(quad, s)
print(f'근: {roots}')  # [-2, 1/2]

# sin(theta) >= 1/2 인 범위: pi/6 <= theta <= 5pi/6
alpha = pi/6
beta = 5*pi/6

result = 3*alpha + beta
result_simplified = sp.simplify(result)
print(f'3α + β = {result_simplified}')
print(f'3α + β = {float(result_simplified/pi)}π')

if sp.simplify(result - 4*pi/3) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')