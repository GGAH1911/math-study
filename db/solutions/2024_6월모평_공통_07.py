import math
a = 8
# 점근선 x = a와 곡선들의 교점
y_A = math.log2(a/4)
y_B = -math.log2(a)
# AB 거리
AB = abs(y_A - y_B)
if abs(AB - 4) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')