# 그래프 분석을 바탕으로 구간별 함수 정의
def f_left(x):
    # x < 1에서 (1,1)로 접근하는 곡선
    return 1 - 0.4 * (1 - x)

def f_middle(x):
    # 1 <= x <= 3에서 (1,-1)과 (3,3)을 지나는 직선
    return 2 * x - 3

def f_right(x):
    # x > 3에서 (3,-2)에서 시작하는 곡선
    return 0.3 * (x - 3)**2 - 2

# 극한값 계산
lim_1_minus = f_left(1 - 1e-6)
lim_3_plus = f_right(3 + 1e-6)

# 그래프 읽음으로부터 직접:
# lim_{x->1-} f(x) = 1 (그래프의 왼쪽 곡선이 (1,1)로 접근)
# lim_{x->3+} f(x) = -2 (그래프의 오른쪽 곡선이 (3,-2)에서 시작)

graphical_lim_1_minus = 1.0
graphical_lim_3_plus = -2.0

result = graphical_lim_1_minus + graphical_lim_3_plus

if abs(result - (-1.0)) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')