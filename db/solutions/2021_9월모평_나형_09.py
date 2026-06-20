import math

# 정현법칙으로 BC 계산
# BC/sin(A) = AB/sin(C)
A_rad = math.radians(45)
B_rad = math.radians(15)
C_rad = math.radians(120)
AB = 8

BC = AB * math.sin(A_rad) / math.sin(C_rad)

# 정확한 값: 8√6/3
expected = 8 * math.sqrt(6) / 3

if math.isclose(BC, expected, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: BC={BC}, expected={expected}')