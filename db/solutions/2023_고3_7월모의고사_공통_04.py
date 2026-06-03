from sympy import Symbol, limit, Piecewise, sqrt
x = Symbol('x', real=True)
# 그래프를 식으로 재현
# x<-1: 좌측 직선, (-1,1) 빈점으로 다가감 => y = x + 2 (이면 x=-1에서 1)
# -1<=x<=0: 직선, (-1,0)->(0,-1) => y = -x - 1
# 0<x<1: 곡선, (0,0) 빈점 -> (1,1) 빈점, sqrt 모양 => y = sqrt(x)
# x=1: f(1)=2 (단독 점)
# x>1: (1,2) -> (2,0)을 지나 더 내려감, 예: y = 2 - 2(x-1)^2 같은 곡선 (검증엔 1-에서만 필요)
left_piece = -x - 1           # -1 < x <= 0 에서 사용 (오른쪽 극한)
right_piece = sqrt(x)         # 0 < x < 1 에서 사용 (왼쪽 극한)
L1 = limit(left_piece, x, -1, '+')
L2 = limit(right_piece, x, 1, '-')
total = L1 + L2
print('VERIFY_PASS' if total == 1 else 'VERIFY_FAIL')
