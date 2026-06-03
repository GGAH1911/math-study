import math
from sympy import pi, symbols, Eq, solve

# 원뿔 부피
V_cone = (1/3) * math.pi * 3**2 * 8
print(f'원뿔 부피: {V_cone/math.pi}π = {24}π')

# 원기둥 높이 구하기
# π * 2^2 * h = 24π
h = 6
V_cylinder = math.pi * 2**2 * h
print(f'원기둥 부피 (h=6): {V_cylinder/math.pi}π')
print(f'부피 일치: {abs(V_cone - V_cylinder) < 1e-10}')

# 원기둥 표면적
r_cyl = 2
S_cylinder = 2 * math.pi * r_cyl**2 + 2 * math.pi * r_cyl * h
S_value = S_cylinder / math.pi

print(f'원기둥 표면적: {S_value}π')
print(f'답: {S_value}π = 32π')
print('VERIFY_PASS' if abs(S_value - 32) < 1e-10 else 'VERIFY_FAIL')