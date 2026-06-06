from math import isclose

CANDIDATE = 42

# ========== 주어진 조건 ==========
angle_BAO = 28  # Given: ∠BAO = 28°
angle_ADC = 40  # Given: ∠ADC = 40°

# ========== 논리 검증 ==========

# AC = BC인 이등변삼각형이고, O가 외심이므로
# OA = OB → △OAB는 이등변삼각형
# ∠OAB = ∠OBA = 28°
angle_OAB = angle_BAO
angle_AOB = 180 - 2 * angle_OAB
assert isclose(angle_AOB, 124), f"Check 1 failed: ∠AOB = {angle_AOB}"

# 원주각 정리: 중심각 = 2 × 원주각
# ∠ACB = ∠AOB / 2
angle_ACB = angle_AOB / 2
assert isclose(angle_ACB, 62), f"Check 2 failed: ∠ACB = {angle_ACB}"

# AC = BC인 이등변삼각형
# ∠BAC = ∠ABC = (180 - ∠ACB) / 2
angle_BAC = (180 - angle_ACB) / 2
angle_ABC = angle_BAC
assert isclose(angle_BAC, 59), f"Check 3 failed: ∠BAC = {angle_BAC}"

# 외심의 성질: ∠AOC = 2 × ∠ABC
angle_AOC = 2 * angle_ABC
assert isclose(angle_AOC, 118), f"Check 4 failed: ∠AOC = {angle_AOC}"

# △OAC는 OA = OC인 이등변삼각형
# ∠OAC = (180 - ∠AOC) / 2
angle_OAC = (180 - angle_AOC) / 2
assert isclose(angle_OAC, 31), f"Check 5 failed: ∠OAC = {angle_OAC}"

# D는 BC 연장선(C 너머) 위의 점
# ∠ACD와 ∠ACB는 보각 관계
# ∠ACD = 180 - ∠ACB
angle_ACD = 180 - angle_ACB
assert isclose(angle_ACD, 118), f"Check 6 failed: ∠ACD = {angle_ACD}"

# △ACD에서 각의 합 = 180°
# ∠CAD = 180 - ∠ACD - ∠ADC
angle_CAD = 180 - angle_ACD - angle_ADC
assert isclose(angle_CAD, 22), f"Check 7 failed: ∠CAD = {angle_CAD}"

# I는 △ACD의 내심
# AI는 ∠CAD의 이등분선
# ∠CAI = ∠CAD / 2
angle_CAI = angle_CAD / 2
assert isclose(angle_CAI, 11), f"Check 8 failed: ∠CAI = {angle_CAI}"

# ========== ∠OAI 계산 ==========
# A를 기준점으로 각도 설정:
# AB 방향: 0°
# AC 방향: ∠BAC = 59°
# AO 방향: ∠BAO = 28°
# AI 방향: ∠BAC + ∠CAI = 70° (AC로부터 이등분선으로 11° 추가)

angle_AI_from_AB = angle_BAC + angle_CAI
angle_AO_from_AB = angle_BAO

# ∠OAI = AI 방향 - AO 방향
angle_OAI_calculated = angle_AI_from_AB - angle_AO_from_AB

# ========== 최종 검증 ==========
if isclose(angle_OAI_calculated, CANDIDATE):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")