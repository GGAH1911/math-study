def f(x):
    # 그래프로 정의된 조각함수
    if x < -1:
        # 좌측 곡선부 (극한 계산에 불필요)
        return None
    elif x == -1:
        return 1  # 좌측 곡선의 끝, 채워진 점 (-1,1)
    elif -1 < x < 0:
        # 열린점 (-1,0) ~ 열린점 (0,1) 선분: y = x+1
        return x + 1
    elif x == 0:
        return 2  # 채워진 점 (0,2)
    elif 0 < x < 1:
        # 채워진 점 (0,2) ~ 채워진 점 (1,1) 선분: y = -x+2
        return -x + 2
    elif x == 1:
        return 1  # 채워진 점 (1,1)
    else:
        # 열린점 (1,-1)에서 (2,0)을 지나는 직선: y = x-2
        return x - 2

eps = 1e-9
L1 = f(-1 + eps)   # lim x->-1+
L2 = f(1 - eps)    # lim x->1-
total = L1 + L2
answer = 1
if abs(total - answer) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
