import sympy as sp
from sympy import symbols, integrate, summation, simplify

n = symbols('n', integer=True, positive=True)
x = symbols('x', real=True)

# 각 구간에서의 함수
def f_n(x_val, n_val):
    return (n_val + 0.5) * x_val - n_val**2 + 0.5

# 각 구간 적분 계산
total = 0
for n_val in range(1, 6):
    a_n = 2*n_val - 1
    a_n1 = 2*(n_val+1) - 1
    
    # 구간 [a_n, a_{n+1}]에서 적분
    integral = integrate((n_val + sp.Rational(1,2))*x - n_val**2 + sp.Rational(1,2), (x, a_n, a_n1))
    total += integral

if total == 145:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')