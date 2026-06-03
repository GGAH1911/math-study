import math

# 주어진 점
A = (-6, 0)
B = (2, -4)

# 내분점 계산 (3:1 비율)
P_x = (3 * B[0] + 1 * A[0]) / 4
P_y = (3 * B[1] + 1 * A[1]) / 4

# 내분점이 y축 위에 있는지 확인
if abs(P_x) < 1e-10:
    # AB의 길이
    AB_length = math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
    expected = 4 * math.sqrt(5)
    
    # 검증
    if abs(AB_length - expected) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')