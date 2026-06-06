from sympy import symbols, solve, discriminant
import math

# 원래 방정식
x = symbols('x')
k = 6

# 교점 조건: -x + k = x^2 - 2x + 6
eq = x**2 - x + (6 - k)
roots = solve(eq, x)

# 판별식이 0 이상인지 확인
discriminant_value = 1 - 4 * (6 - k)

if len(roots) > 0:
    # 교점이 존재하면 직선 위의 점들이 포물선 위의 점들과 일치하는지 확인
    verified = True
    for root in roots:
        y_line = -root + k
        y_parabola = root**2 - 2*root + 6
        if abs(float(y_line - y_parabola)) > 1e-9:
            verified = False
    if verified:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')