import math
a = 3
b = 3
# 점근선 확인
asymptote = a
if asymptote == 3:
    # 점 (7, b)를 지나는지 확인
    y_at_7 = math.log2(7 - a) + 1
    if abs(y_at_7 - b) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')