import sympy as sp
x, m, b = sp.symbols('x m b')
# 원래 조건: 직선 y = m*x + b 가 (1,-1)과 (2,1)을 지난다
eq1 = sp.Eq(m*1 + b, -1)
eq2 = sp.Eq(m*2 + b, 1)
sol = sp.solve([eq1, eq2], [m, b])
# 내 답: y절편 = -3
my_answer = -3
if sp.simplify(sol[b] - my_answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')