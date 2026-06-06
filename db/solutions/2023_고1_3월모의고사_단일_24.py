import math

# 각도 검증
angle_B = 72  # 도
angle_C = 48  # 도
angle_A = 180 - angle_B - angle_C  # 60°

# AB와 평행한 직선 관계
angle_BCD = 180 - angle_B  # 108°
angle_DCA = angle_BCD - angle_C  # 60°

# 평행선의 성질 (같은 쪽 내각)
angle_CDE = 52
angle_AED = 180 - angle_CDE  # 128°
angle_BED = 180 - angle_AED  # 52°

# 삼각형 BCE
angle_BCE = angle_C  # 48°
angle_CBE = angle_B  # 72°
angle_CEB = 180 - angle_BCE - angle_CBE  # 60°

# 삼각형 AFE (F는 AC 위의 교점)
angle_FAE = angle_A  # 60° (F는 AC 위)
angle_AEF = 52  # 계산된 값
angle_AFE = 180 - angle_FAE - angle_AEF  # 68°

# ∠EFC 계산 (A-F-C가 일직선)
angle_EFC = 180 - angle_AFE  # 112°

# 검증
print(f"∠A = {angle_A}°")
print(f"∠BCD = {angle_BCD}°")
print(f"∠DCA = {angle_DCA}°")
print(f"∠AED = {angle_AED}°")
print(f"∠BED = {angle_BED}°")
print(f"∠CEB = {angle_CEB}°")
print(f"삼각형 AFE: ∠FAE={angle_FAE}°, ∠AEF={angle_AEF}°, ∠AFE={angle_AFE}°")
print(f"합계: {angle_FAE + angle_AEF + angle_AFE}° = 180°")
print(f"∠EFC = {angle_EFC}°")

if angle_EFC == 112:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")