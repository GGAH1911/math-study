import numpy as np
from sympy import sin, cos, pi, simplify, symbols

# 정답 확인
alpha = pi/6
beta = 5*pi/6
answer = 4*beta - 2*alpha
print(f'Result: {simplify(answer)}')

# 판별식이 경계값에서 0인지 확인
def discriminant(theta):
    s = sin(theta)
    return -8*s**2 + 20*s - 8

D_alpha = simplify(discriminant(alpha))
D_beta = simplify(discriminant(beta))
D_mid = simplify(discriminant(pi/2))

print(f'D(α=π/6) = {D_alpha}')  # 0
print(f'D(β=5π/6) = {D_beta}')  # 0
print(f'D(π/2) = {D_mid}')  # > 0

if float(D_alpha) >= -1e-10 and float(D_beta) >= -1e-10 and float(D_mid) >= 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')