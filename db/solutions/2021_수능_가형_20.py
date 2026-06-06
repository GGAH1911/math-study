import numpy as np

n = 16

# 연속성 조건: g는 I_j=(j/(2n),(j+1)/(2n))에서 상수
# 조건1에서 유일하게 결정: g_j=1(짝수 j), g_j=0(홀수 j)
# 해석적 공식:
#   ∫_{I_j} π sin(2πnx) dx = (-1)^j / n
#   ∫_{I_j} x·π sin(2πnx) dx = (-1)^j*(2j+1)/(4n^2)

integral_h = 0.0
integral_xh = 0.0

for j in range(-2*n, 2*n):
    gj = 1 if j % 2 == 0 else 0
    sign_j = (-1)**j
    integral_h += gj * sign_j / n
    integral_xh += gj * sign_j * (2*j + 1) / (4 * n**2)

check1 = abs(integral_h - 2.0) < 1e-9
check2 = abs(integral_xh - (-1.0/32)) < 1e-9

if check1 and check2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: integral_h={integral_h}, integral_xh={integral_xh}')
