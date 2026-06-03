import sympy as sp

x = sp.Symbol('x', real=True)

# 그래프 좌측 곡선 [-2, -1): (-2,0) 닫힌점에서 (-1,3) 열린점으로 가는 포물선
# f1(x) = -3x(x+2): f1(-2)=0, lim x->-1- f1 = 3
f_left = -3*x*(x + 2)

# 그래프 우측 직선 (1, 2]: (1,2) 닫힌점에서 (2,0) 닫힌점
# f2(x) = -2(x-2): f2(1)=2, f2(2)=0
f_right = -2*(x - 2)

# 한쪽 극한 계산
lim_left  = sp.limit(f_left, x, -1, '-')
lim_right = sp.limit(f_right, x,  1, '+')

total = sp.simplify(lim_left + lim_right)

answer = 5
if total == answer and lim_left == 3 and lim_right == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
