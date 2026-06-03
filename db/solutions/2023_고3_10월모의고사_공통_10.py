import sympy as sp
from sympy import symbols, sqrt, solve, limit, oo

t = symbols('t', positive=True, real=True)
x = symbols('x', real=True)

# 직선과 곡선의 교점
line = t*x + t + 1
curve = x**2 - t*x - 1

# 교점 방정식
eq = line - curve
eq_simplified = sp.expand(eq)
# x^2 - 2tx - 2 = 0

# 근 구하기
roots = solve(eq, x)
x1, x2 = roots[0], roots[1]

# y좌표
y1 = line.subs(x, x1)
y2 = line.subs(x, x2)

# 거리
dist_sq = (x2 - x1)**2 + (y2 - y1)**2
dist = sqrt(sp.expand(dist_sq))
dist_simplified = sp.simplify(dist)

# 극한 계산
result = limit(dist_simplified / t**2, t, oo)
print(f'극한값: {result}')

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')