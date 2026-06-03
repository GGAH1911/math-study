import sympy as sp

# 그래프 정의 (구간별)
# x <= -1: 좌측 직선, 닫힌 점 (-1, 0) 에서 끝남. 예: y = x + 1
# -1 < x <= 0: (-1, 2) 열린점 ~ (0, 1) 닫힌점 잇는 직선: y = -x + 1
# 0 < x <= 1: (0, -1) 열린점 ~ (1, 2) 닫힌점 잇는 곡선 (예: 3x - 1)
# x > 1: (1, 0) 열린점 시작 직선 (예: y = x - 1)

x = sp.Symbol('x', real=True)

# 좌극한: x -> -1- 일 때 좌측 직선 식 사용
f_left = x + 1  # 닫힌 점 (-1, 0)을 지나는 좌측 직선
lim_neg1_minus = sp.limit(f_left, x, -1, '-')

# 우극한: x -> 0+ 일 때 (0, 1] 구간 곡선 식 사용 (0에서 -1로 접근)
f_right = 3*x - 1  # 곡선 형태는 달라도 x->0+ 에서 -1 로 접근
lim_0_plus = sp.limit(f_right, x, 0, '+')

total = lim_neg1_minus + lim_0_plus
proposed_answer = -1

if sp.simplify(total - proposed_answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
