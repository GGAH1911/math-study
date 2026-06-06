import math

x = 9

# 정의역 확인
assert x > 5, f"x={x}는 정의역을 만족하지 않음"
assert x > -7, f"x={x}는 정의역을 만족하지 않음"

# 원래 방정식에 대입
left = math.log2(x - 5)
right = math.log(x + 7) / math.log(4)

# 수치 오차 범위 내 일치 확인
if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')