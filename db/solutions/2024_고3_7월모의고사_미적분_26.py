import math
from fractions import Fraction

# u = 1/3 일 때 검증
u = Fraction(1, 3)

# tan(∠CFE) 검증
numerator = u**2 - u + 2
denominator = 2 - u
tan_CFE = numerator / denominator
print(f'tan(∠CFE) = {tan_CFE} (should be 16/15)')
assert tan_CFE == Fraction(16, 15), f'Expected 16/15, got {tan_CFE}'

# 좌표
D = (Fraction(2, 3), 0)
C = (0, 1)
B = (0, 0)

# 벡터
DC = (C[0] - D[0], C[1] - D[1])
DB = (B[0] - D[0], B[1] - D[1])
print(f'DC = {DC}')
print(f'DB = {DB}')

# 외적 (2D: scalar)
cross = DC[0] * DB[1] - DC[1] * DB[0]
print(f'cross product = {cross}')

# 내적
dot = DC[0] * DB[0] + DC[1] * DB[1]
print(f'dot product = {dot}')

# tan(∠CDB)
tan_CDB = abs(cross) / dot
print(f'tan(∠CDB) = {tan_CDB}')
assert tan_CDB == Fraction(3, 2), f'Expected 3/2, got {tan_CDB}'

# 각도 범위 검증: π/4 < ∠CDB < π/2
angle_CDB = math.atan(float(tan_CDB))
pi_4 = math.pi / 4
pi_2 = math.pi / 2
print(f'∠CDB = {math.degrees(angle_CDB):.2f}° (should be between 45° and 90°)')
assert pi_4 < angle_CDB < pi_2, f'Angle constraint violated'

print('VERIFY_PASS')