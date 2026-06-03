import sympy as sp
x = sp.Symbol('x')
# 직선 y = 2x + 2
# 첫 번째 포물선과의 교점
eq1 = sp.Eq(2*x + 2, x**2/3 + 5)
sol1 = sp.solve(eq1, x)
print('첫 번째 포물선 교점:', sol1, '중근 여부:', len(sol1) == 1 or sol1[0] == sol1[1] if len(sol1) > 1 else True)
# 두 번째 포물선과의 교점 (n=3)
eq2 = sp.Eq(2*x + 2, x**2 + 4*x + 3)
sol2 = sp.solve(eq2, x)
print('두 번째 포물선 교점:', sol2, '중근 여부:', len(sol2) == 1 or sol2[0] == sol2[1] if len(sol2) > 1 else True)
if len(sol1) == 1 and len(sol2) == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')