import math

# 최솟값 조건으로부터 a 구하기
# f(a) = log_2(2a) + 1 = 3 ⟹ a = 2
a = 2

# 검증: 최솟값이 3인지 확인
min_val = math.log2(2*a) + 1
if abs(min_val - 3.0) < 1e-9:
    # f(a+4) 계산
    answer_val = math.log2(a + 4 + a) + 1
    # 답이 4인지 확인
    if abs(answer_val - 4.0) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')