from sympy import *
x = symbols('x', positive=True)
# 포물선 y^2=12x, 초점 (3,0), 준선 x=-3
# PF = x + 3 (포물선 정의)
eq = Eq(x + 3, 9)
sol = solve(eq, x)
x_val = sol[0]
# 검산: 실제 거리 계산
y_sq = 12 * x_val
PF = sqrt((x_val - 3)**2 + y_sq)
if PF == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')