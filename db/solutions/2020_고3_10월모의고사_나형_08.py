from sympy import symbols, limit, oo

CANDIDATE = 6

# 그래프 함수 정의
# x <= 0: f(x) = 4
# 0 < x <= 1: f(x)는 (0,0)에서 (1,2)로 가는 곡선
# 1 < x < 2: f(x)는 (1,2)에서 (2,0)으로 가는 곡선
# x >= 2: f(x) < 0

# 극한 계산
# lim(x->1+) f(x) = 2 (그래프에서 직접 읽음)
limit_1_right = 2

# lim(x->0-) f(x)/(x-1) 계산
# x->0-일 때 f(x) = 4, x-1 = -1
limit_0_left = 4 / (-1)  # = -4

# 최종 계산
result = limit_1_right - limit_0_left

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')