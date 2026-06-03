# 이미지의 그래프 정보를 그대로 코드화
# 왼쪽 구간 [-2, 0): (-2,0)에서 (0,1)로 가는 곡선 (예: f(x) = sqrt((x+2)/2) 형태로 (-2,0)→(0,1))
# 가운데 구간 (0,1]: (0,0) 열린점에서 (1,1) 닫힌점으로 가는 직선
# 오른쪽 구간 (1,2]: (1,2) 열린점에서 (2,-1) 닫힌점으로 가는 직선
import math

def f_left(x):
    # 단조증가 곡선, x=-2에서 0, x→0-에서 1로 수렴
    return math.sqrt((x + 2) / 2)

def f_right_of_1(x):
    # (1,2) → (2,-1) 직선: 기울기 -3, y = 2 - 3(x-1) = 5 - 3x
    return 5 - 3*x

# 좌극한 x→0-
eps = 1e-8
L1 = f_left(0 - eps)
# 우극한 x→1+
L2 = f_right_of_1(1 + eps)

result = L1 - L2
expected = -1

if abs(result - expected) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
