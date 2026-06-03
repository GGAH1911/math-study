import sympy as sp
from sympy import symbols, I, expand, solve

# 원래 방정식 x^2 + ax + b = 0에서 a=-2, b=2
a, b = -2, 2
x = symbols('x')

# 방정식
eq = x**2 + a*x + b

# 근 계산
roots = solve(eq, x)
print(f'근: {roots}')

# 한 근이 b/2 + i 인지 확인
target_root = b/2 + I
print(f'목표 근: {target_root}')
print(f'근 중 일치 여부: {target_root in roots}')

# 검증
for root in roots:
    result = eq.subs(x, root)
    print(f'x={root}을 대입: {expand(result)}')

product = a * b
print(f'\nab = {product}')
if product == -4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')