import sympy as sp
x, y = sp.symbols('x y', real=True)
ellipse = x**2/9 + y**2/4 - 1
# 단축은 y축 방향 (a^2=9 > b^2=4 이므로 단축은 짧은 축인 y축). 양 끝점 (0, b), (0, -b) 찾기.
sols = sp.solve(ellipse.subs(x, 0), y)
length = abs(sols[0] - sols[1])
# 또 x축 방향 길이도 비교해서 더 짧은 쪽이 단축
sols_x = sp.solve(ellipse.subs(y, 0), x)
length_x = abs(sols_x[0] - sols_x[1])
minor = sp.Min(length, length_x)
print('VERIFY_PASS' if sp.simplify(minor - 4) == 0 else 'VERIFY_FAIL')