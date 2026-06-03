import numpy as np

# 풀이에서 구한 값: a=BC=8, b=CA=5, c=AB=7
a, b, c = 8, 5, 7

# 조건1: AB = 7
assert c == 7, f'AB={c} != 7'

# 조건2: C = 60도 (angle AIB = 90 + C/2 = 120)
cosC = (a**2 + b**2 - c**2) / (2*a*b)
C_deg = np.degrees(np.arccos(cosC))
assert abs(C_deg - 60.0) < 1e-9, f'C={C_deg} != 60'

# angle AIB = 90 + C/2
angle_AIB = 90 + C_deg / 2
assert abs(angle_AIB - 120.0) < 1e-9, f'angle_AIB={angle_AIB} != 120'

# 조건3: D는 내접원과 CA의 접점 -> AD = s - a = 2
s = (a + b + c) / 2
AD = s - a
assert abs(AD - 2.0) < 1e-9, f'AD={AD} != 2'

# 둘레 확인
perimeter = a + b + c
assert perimeter == 20, f'perimeter={perimeter} != 20'

print('VERIFY_PASS')
print(f'a=BC={a}, b=CA={b}, c=AB={c}, perimeter={perimeter}')
