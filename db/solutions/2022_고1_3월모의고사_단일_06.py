import math

# 주어진 조건
angle_OBC = 17  # 도
angle_OCA = 52  # 도

# 외심 성질: 이등변삼각형
angle_OCB = angle_OBC  # 17도
angle_OAC = angle_OCA  # 52도

# 중심각 계산
angle_BOC = 180 - angle_OBC - angle_OCB
angle_COA = 180 - angle_OCA - angle_OAC
angle_AOB = 360 - angle_BOC - angle_COA

# 우리의 답
angle_OAB = 21
angle_OBA = angle_OAB  # 이등변삼각형

# 검증: 삼각형 OAB의 내각 합
triangle_OAB_sum = angle_OAB + angle_OBA + angle_AOB

# 검증: 삼각형 ABC의 내각 합
angle_BAC = angle_OAB + angle_OAC
angle_ABC = angle_OBA + angle_OBC
angle_ACB = angle_OCA + angle_OCB
triangle_ABC_sum = angle_BAC + angle_ABC + angle_ACB

if triangle_OAB_sum == 180 and triangle_ABC_sum == 180:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')