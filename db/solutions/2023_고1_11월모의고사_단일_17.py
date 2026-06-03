import sympy as sp
from sympy import symbols, solve, sqrt

x = symbols('x')
k_val = 3
f = -x**2 + 4*x + k_val + 3
line = 2*x + 3

# 교점 확인
intersections = solve(f - line, x)
print(f"교점 x좌표: {intersections}")
alpha, beta = -1, 3

# 함수값 확인
f_alpha = f.subs(x, alpha)
f_beta = f.subs(x, beta)
f_max = f.subs(x, 2)
print(f"f(-1) = {f_alpha}")
print(f"f(3) = {f_beta}")
print(f"f(2) = {f_max}")

# 최댓값이 10인지 확인
if f_max == 10 and f_alpha == 1 and f_beta == 9:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")