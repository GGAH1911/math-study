import sympy as sp
x = sp.Symbol('x')
m_val = 3
# 직선: y = m(x+1) = 3x + 3
line = 3*x + 3
# 곡선: y = x^2 + x + 4
curve = x**2 + x + 4
# 교점 방정식
eq = curve - line
sol = sp.solve(eq, x)
# 접할 조건: 중근 (해가 1개)
if len(sol) == 1 or (len(sol) == 2 and sol[0] == sol[1]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')