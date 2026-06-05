import sympy as sp
import math

x = sp.Symbol('x', positive=True, real=True)

# 곡선 정의
y = sp.sqrt(x * (1 + sp.ln(x)))

# y^2를 정적분
y_squared = x + x*sp.ln(x)
integral_y2 = sp.integrate(y_squared, (x, 1, 2))

# 정삼각형 단면 넓이: sqrt(3)/4 * y^2
area = sp.sqrt(3) / 4 * y_squared
volume = sp.integrate(area, (x, 1, 2))

# 답과 비교
answer_numerical = float(sp.sqrt(3) * (3 + 8*sp.ln(2)) / 16)
volume_numerical = float(volume)

if abs(volume_numerical - answer_numerical) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')