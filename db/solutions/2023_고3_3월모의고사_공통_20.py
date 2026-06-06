import sympy as sp
from sympy import symbols, diff, integrate, solve

# 원래 문제의 함수 정의
x, p = symbols('x p', real=True, positive=True)
f = lambda t: t**3 - 12*t + 1

# p = 2로 계산됨
p_val = 2

# g(x) 정의
def g_func(x_val, p_val):
    if x_val >= 0:
        return f(x_val + p_val) - f(p_val)
    else:
        return f(x_val - p_val) - f(-p_val)

# 적분 검증
from scipy import integrate as sp_integrate
integral_result = sp_integrate.quad(lambda x_val: x_val**3 + 3*p_val*x_val**2, 0, p_val)[0]

# f(5) 계산
f_5 = f(5)

# 검증
assert abs(integral_result - 20) < 1e-9, f'Integral check failed: {integral_result}'
assert f_5 == 66, f'f(5) check failed: {f_5}'

print('VERIFY_PASS')