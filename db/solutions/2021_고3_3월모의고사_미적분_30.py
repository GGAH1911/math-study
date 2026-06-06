import sympy as sp
from sympy import symbols, expand, limit, oo, sqrt

n = symbols('n', positive=True, integer=True)

# f(x) 정의
x = symbols('x')
f = x*(x-n)*(x-3*n**2)

# f'(x) 계산
f_prime = sp.diff(f, x)

# a_n 계산 (극대값)
a_n_expr = ((n + 3*n**2) - n*sqrt(1 - 3*n + 9*n**2))/3

# 큰 n에서 a_n 근사
a_n_approx = n/2 - 1/24

# b_n 계산
b_n = n + 3*n**2 - 2*a_n_expr

# a_n * b_n 계산
a_n_b_n = a_n_expr * b_n

# 극한 계산
ratio = a_n_b_n / n**3
lim_val = limit(ratio, n, oo)

if abs(lim_val - 3/2) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')