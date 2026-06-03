# 그래프로부터 읽은 극한값
lim_0_minus = 2  # 열린 원점 (0, 2)
lim_1_plus = 1   # 채워진 점 (1, 1)에서 오른쪽 연속

# 극한값의 차
result = lim_0_minus - lim_1_plus

if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')