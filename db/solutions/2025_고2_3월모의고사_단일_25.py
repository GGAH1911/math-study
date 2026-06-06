import math

# 원함수: y = sqrt(2(x-1)) + a
# a = 5로 구함
a = 5

# 역함수의 그래프가 (5, 1)을 지나면 원함수는 (1, 5)를 지남
x1, y1_expected = 1, 5
y1_actual = math.sqrt(2 * (x1 - 1)) + a
if abs(y1_actual - y1_expected) > 1e-9:
    print('VERIFY_FAIL')
else:
    # 역함수의 그래프가 (b, 3)을 지나면 원함수는 (3, b)를 지남
    x2 = 3
    y2_actual = math.sqrt(2 * (x2 - 1)) + a
    b = y2_actual
    
    # 확인: 역함수가 (b, 3)을 지나는가?
    # 즉, 원함수가 (3, b)를 지나는가?
    if abs(y2_actual - b) < 1e-9:  # y2_actual은 b의 정의이므로 항상 참
        result = a + b
        if abs(result - 12) < 1e-9:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')