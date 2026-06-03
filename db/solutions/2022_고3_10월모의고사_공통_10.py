import math

a = 5/4
x1, x2 = -1/2, -2
y1 = -math.log2(-x1)
y2 = -math.log2(-x2)

# 원래 함수에 대입해서 검증
y1_check = math.log2(x1 + 2*a)
y2_check = math.log2(x2 + 2*a)

if abs(y1 - y1_check) < 1e-10 and abs(y2 - y2_check) < 1e-10:
    # 거리 계산
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if abs(dist - 5/2) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')