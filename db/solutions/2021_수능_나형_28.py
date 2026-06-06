import math
k_squared = 21
k = math.sqrt(k_squared)
AC = k
AB = 3 * k
angle_A = math.pi / 3
R = 7

# 코사인 법칙으로 BC 계산
BC_squared = AB**2 + AC**2 - 2 * AB * AC * math.cos(angle_A)
BC = math.sqrt(BC_squared)

# 사인 법칙 검증: BC / sin(A) = 2R
sin_A = math.sin(angle_A)
ratio = BC / sin_A
expected_ratio = 2 * R

if abs(BC_squared - 147) < 1e-9 and abs(ratio - expected_ratio) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')