import math

# 변환된 함수: y = log_3(x-2) + 5
# 점 (5, a)를 지남
x_point = 5
a = math.log(x_point - 2, 3) + 5

# a가 6인지 확인
expected_a = 6

if abs(a - expected_a) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')