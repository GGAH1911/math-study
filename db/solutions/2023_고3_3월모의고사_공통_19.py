import sympy as sp

t = sp.Symbol('t', real=True)
k = 18

# 위치 함수: 원점 출발 (적분상수 = 0)
x1 = sp.integrate(3*t**2 - 15*t + k, t)
x2 = sp.integrate(-3*t**2 + 9*t, t)

# 만나는 조건
eq = x1 - x2
solutions = sp.solve(eq, t)

# t > 0인 해의 개수
positive_solutions = [s for s in solutions if s > 0]

if len(positive_solutions) == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')