import sympy as sp

x = sp.Symbol('x', real=True)

# 그래프에서 읽은 f(x)의 각 구간
f_left  = sp.Integer(4)   # x < 0: 수평선 y=4
f_mid   = 4*x**2          # 0<=x<=1: (0,0)->(1,4) 위로 볼록한 곡선 (극한에는 무관)
f_right = 4 - 2*x         # x > 1: (1,2) 빈점과 (2,0)을 지나는 직선

# 첫째 항: x -> 1+  (오른쪽 분기)
lim1 = sp.limit(f_right, x, 1, dir='+')

# 둘째 항: x -> 0-  의 f(x)/(x-1)  (왼쪽 분기 f=4)
expr2 = f_left/(x-1)
lim2 = sp.limit(expr2, x, 0, dir='-')

result = sp.simplify(lim1 - lim2)

# 분기 일관성 점검
assert lim1 == 2, lim1
assert lim2 == -4, lim2

CANDIDATE = 6
if sp.simplify(result - CANDIDATE) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')