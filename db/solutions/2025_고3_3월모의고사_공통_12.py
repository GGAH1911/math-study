import sympy as sp
from sympy import symbols, integrate, solve, diff, Rational

x = symbols('x')
f = x**3 + 2*x**2 - x + 4
f_prime = diff(f, x)

# 접점 찾기: f(a) = a*f'(a)
a = symbols('a')
eq = f.subs(x, a) - a * f_prime.subs(x, a)
sol_a = solve(eq, a)
print(f'접점 a: {sol_a}')

# a=1에서의 f(1)
f_1 = f.subs(x, 1)
print(f'f(1) = {f_1}')

# 접선: y = 6x
slope = f_prime.subs(x, 1)
print(f'접선의 기울기: {slope}')

# 구간 [-2, 0]에서 곡선 아래 넓이
area1 = integrate(f, (x, -2, 0))
print(f'Area 1 [-2, 0]: {area1}')

# 구간 [0, 1]에서 곡선과 접선 사이 넓이
g = f - 6*x
area2 = integrate(g, (x, 0, 1))
print(f'Area 2 [0, 1]: {area2}')

# 전체 넓이
total_area = area1 + area2
print(f'Total area: {total_area}')
print(f'Total area = {float(total_area)}')

if total_area == Rational(51, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')