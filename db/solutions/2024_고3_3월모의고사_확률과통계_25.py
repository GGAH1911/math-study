import math

# 여학생 2명을 하나의 단위로 묶으면:
# 총 6개의 단위가 원탁에 앉음
# 원탁 배치 (회전을 같은 것으로 봄): (6-1)!
arranged_units = math.factorial(5)  # = 120

# 여학생 2명 내에서의 순서
internal_arrangement = math.factorial(2)  # = 2

# 최종 경우의 수
total = arranged_units * internal_arrangement  # = 240

if total == 240:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')