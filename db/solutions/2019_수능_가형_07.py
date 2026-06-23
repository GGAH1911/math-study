from sympy import symbols, exp, diff, E, simplify

x, y = symbols('x y', real=True)

# 곡선 방정식을 F(x, y) = 0 형태로: e^x - x*e^y - y = 0
F = exp(x) - x*exp(y) - y

# 음함수 미분: dy/dx = -F_x / F_y
F_x = diff(F, x)
F_y = diff(F, y)

# 점 (0, 1)에서의 기울기
slope = -F_x.subs([(x, 0), (y, 1)]) / F_y.subs([(x, 0), (y, 1)])

# 정답: 1 - e
answer = 1 - E

# 검증
if simplify(slope - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')