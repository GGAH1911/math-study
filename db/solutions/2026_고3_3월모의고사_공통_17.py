import sympy as sp
x = sp.Symbol('x')
# 원래 함수
f = 4*x**3 - 3*x**2 + 2
# 부정적분
F_general = sp.integrate(f, x)
# C를 변수로 두고 초기조건 적용
C = sp.Symbol('C')
F = F_general + C
C_val = sp.solve(F.subs(x, 1) - 5, C)[0]
F_final = F.subs(C, C_val)
result = F_final.subs(x, 2)
if result == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')