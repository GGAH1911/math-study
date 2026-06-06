import math
from math import sqrt

# 좌표 설정
C = (0, 0)
B = (30, 0)
A = (0, 16)
M = (15, 8)
N = (15, 0)
D = (15, -9)

# 벡터 DA, DC
DA = (-15, 25)
DC = (-15, 9)

# cos(∠ADC) 계산
dot_product = DA[0]*DC[0] + DA[1]*DC[1]
mag_DA = sqrt(DA[0]**2 + DA[1]**2)
mag_DC = sqrt(DC[0]**2 + DC[1]**2)

cos_x = dot_product / (mag_DA * mag_DC)

# sin x 계산
sin_x = sqrt(1 - cos_x**2)

# 8/17과 비교
expected_sin = 8/17

if abs(sin_x - expected_sin) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')