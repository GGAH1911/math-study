import math

# 원주각이 65도일 때, 중심각은 130도
central_angle = 2 * 65
assert central_angle == 130, f"중심각 계산 오류: {central_angle}"

# 사각형 OAPB에서 내각의 합
# ∠OAP = 90 (접선), ∠AOB = 130 (중심각), ∠OBP = 90 (접선)
angle_OAP = 90
angle_AOB = 130
angle_OBP = 90

angle_APB = 360 - angle_OAP - angle_AOB - angle_OBP
assert angle_APB == 50, f"∠APB 계산 오류: {angle_APB}"

print('VERIFY_PASS')