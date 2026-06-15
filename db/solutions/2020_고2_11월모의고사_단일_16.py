import sympy as sp
from sympy import sin, cos, tan, sqrt, symbols, solve, simplify

theta = symbols('theta', real=True)

# 조건: 3*sin(θ) - 4*tan(θ) = 4
condition = 3*sin(theta) - 4*tan(theta) - 4

# sin(θ) + cos(θ) = -1/3 검증
# sin(θ) + cos(θ) = -1/3이면
# sin(θ)cos(θ) = -4/9
# sin(θ), cos(θ)는 t^2 + (1/3)t - 4/9 = 0의 근

t = symbols('t')
quad_eq = t**2 + sp.Rational(1,3)*t - sp.Rational(4,9)
roots = solve(quad_eq, t)

sin_val = roots[0]
cos_val = roots[1]

print(f'sin(θ) = {sin_val}')
print(f'cos(θ) = {cos_val}')
print(f'sin(θ) + cos(θ) = {simplify(sin_val + cos_val)}')
print(f'sin(θ)cos(θ) = {simplify(sin_val * cos_val)}')

# 원래 조건 검증
lhs = 3*sin_val - 4*(sin_val/cos_val)
result = simplify(lhs)
print(f'3sin(θ) - 4tan(θ) = {result}')

if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')