import sympy as sp

k = 14
x = sp.Symbol('x')

# 교점 찾기: x^2 - 2x = 3x + k
eq = x**2 - 2*x - (3*x + k)
roots = sp.solve(eq, x)
roots.sort()
x_P, x_Q = roots[0], roots[1]

# y좌표 확인
y_P_parabola = x_P**2 - 2*x_P
y_P_line = 3*x_P + k
y_Q_parabola = x_Q**2 - 2*x_Q
y_Q_line = 3*x_Q + k

assert y_P_parabola == y_P_line, f'P not on line: {y_P_parabola} != {y_P_line}'
assert y_Q_parabola == y_Q_line, f'Q not on line: {y_Q_parabola} != {y_Q_line}'

# 내분점 x좌표
x_div = (2*x_P + x_Q) / 3

if x_div == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')