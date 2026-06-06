# 원래 문제: y = (5-2k)x + 2 와 y = x + 3 이 평행
# 평행 조건: 기울기가 같아야 함
k = 2
slope1 = 5 - 2*k  # 첫 번째 직선의 기울기
slope2 = 1         # 두 번째 직선의 기울기
if slope1 == slope2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')