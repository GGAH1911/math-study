import math

# 외접원의 반지름을 1로 정규화
R = 1
O = (0, 0)
B = (1, 0)

# ∠BOC = 104°
angle_BOC_rad = math.radians(104)
C = (math.cos(angle_BOC_rad), math.sin(angle_BOC_rad))

# BC의 길이
BC = math.sqrt((B[0] - C[0])**2 + (B[1] - C[1])**2)

# BD = BC 조건으로부터 D의 x좌표 (BO의 연장선 위)
# D = (t, 0) where |1 - t| = BC and t < 0
t = 1 - BC  # t < 0이므로
D = (t, 0)

# BD 검증
BD = abs(B[0] - D[0])

# ∠OCD 계산
CO = (O[0] - C[0], O[1] - C[1])
CD = (D[0] - C[0], D[1] - C[1])

# 내적
dot_product = CO[0]*CD[0] + CO[1]*CD[1]

# 크기
mag_CO = math.sqrt(CO[0]**2 + CO[1]**2)
mag_CD = math.sqrt(CD[0]**2 + CD[1]**2)

# 코사인
cos_OCD = dot_product / (mag_CO * mag_CD)
angle_OCD_rad = math.acos(cos_OCD)
angle_OCD = math.degrees(angle_OCD_rad)

# 답이 33도 근처인지 확인
if 32 < angle_OCD < 34:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Calculated angle: {angle_OCD:.1f}°')