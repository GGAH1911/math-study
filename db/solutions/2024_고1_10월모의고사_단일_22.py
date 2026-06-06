# 두 점을 지나는 직선의 기울기
a = 3
slope1 = (2*a + 1 - a) / (2 - 0)
slope2 = 2

# 두 직선이 평행한지 확인 (기울기가 같은지)
if abs(slope1 - slope2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')