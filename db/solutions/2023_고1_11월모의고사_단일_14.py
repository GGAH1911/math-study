import sympy as sp
from sympy import sqrt, Abs

# 검증: a=2, b=2일 때
a, b = 2, 2

# 원: (x-1)^2 + (y-1)^2 = 2+b = 4
r = sqrt(2 + b)
assert r == 2, f"반지름이 2가 아님: {r}"

# 직선과 원의 교점 A, B
x = sp.Symbol('x')
eq = (x - 1)**2 + (2*x - 1 - 1)**2 - 4
roots = sp.solve(eq, x)
A = (roots[0], 2*roots[0] - 1)
B = (roots[1], 2*roots[1] - 1)

# AB의 길이
AB_length = sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
assert AB_length == 4, f"AB 길이가 4가 아님: {AB_length}"

# 점 P에서 직선까지 최대 거리 = 반지름
max_dist_to_line = r

# 삼각형 ABP의 최대 넓이
max_area = sp.Rational(1, 2) * AB_length * max_dist_to_line
assert max_area == 4, f"최대 넓이가 4가 아님: {max_area}"

print('VERIFY_PASS')