import sympy as sp
x = sp.Symbol('x')
# 새로 추가된 부분 = 전체 - 원래 정사각형
added_area = (10 + x) * x - 100
eq = sp.Eq(added_area, 500)
sol = sp.solve(eq, x)
valid_sol = [s for s in sol if s > 10][0]
result = (10 + valid_sol) * valid_sol - 100
if abs(result - 500) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')