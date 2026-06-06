import numpy as np
from scipy.optimize import fminbound
from sympy import symbols, diff, solve, expand

# 문제의 원래 함수
x = symbols('x', real=True)
f = 3*x**4 - 4*x**3 - 12*x**2

# 미분하여 임계점 찾기
f_prime = diff(f, x)
critical_points = solve(f_prime, x)
print(f"임계점: {critical_points}")

# 각 임계점에서의 함수값
f_func = lambda t: float(f.subs(x, t))
values = {float(cp): f_func(cp) for cp in critical_points}
print(f"임계점에서의 함수값: {values}")

# 최솟값
min_val = min(values.values())
print(f"f(x)의 최솟값: {min_val}")

# k의 최솟값
k_min = -min_val
print(f"k의 최솟값: {k_min}")

# 검증: k = 32일 때 3x^4 - 4x^3 - 12x^2 + 32 >= 0인지 확인
k = 32
inequality = 3*x**4 - 4*x**3 - 12*x**2 + k
inequality_func = lambda t: 3*t**4 - 4*t**3 - 12*t**2 + 32

# 임계점에서의 부등식 값 확인
for cp in critical_points:
    val = inequality_func(float(cp))
    print(f"x={float(cp)}: {3*float(cp)**4 - 4*float(cp)**3 - 12*float(cp)**2 + 32}")

# 수치적으로 최솟값 찾기 (- infinity에서 +infinity 범위)
min_inequality_value = fminbound(inequality_func, -10, 10)
min_inequality_value = inequality_func(min_inequality_value)
print(f"부등식의 최솟값: {min_inequality_value}")

if min_inequality_value >= -1e-10:  # 수치 오차 고려
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")