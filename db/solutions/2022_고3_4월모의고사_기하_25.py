from sympy import *
c = symbols('c', positive=True)
# 포물선: y^2=4cx, FP=x_P+c=8, y_P=6 (넓이 조건)
x_P_expr = 8 - c
y_P = 6
# 포물선 방정식: y_P^2 = 4c*x_P
eq = Eq(y_P**2, 4*c*x_P_expr)
c_sols = solve(eq, c)
results = []
for cv in c_sols:
    cv = float(cv)
    xp = 8 - cv
    # FP 검증
    FP = float(sqrt((xp - cv)**2 + y_P**2))
    # 삼각형 넓이 검증
    area = 0.5 * (xp + cv) * y_P
    # F'P
    FpP = float(sqrt((xp + cv)**2 + y_P**2))
    two_a = FP + FpP
    results.append((abs(FP - 8) < 1e-9, abs(area - 24) < 1e-9, abs(two_a - 18) < 1e-9))
if all(r[0] and r[1] and r[2] for r in results):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', results)
