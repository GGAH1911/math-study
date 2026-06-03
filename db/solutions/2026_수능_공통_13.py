import numpy as np

def f(x):
    return x**2 - 4*x - 3

def g(x):
    return (x**3 - 2*x) * f(x)

def f_prime(x):
    return 2*x - 4

def g_prime(x):
    return (3*x**2 - 2)*(x**2 - 4*x - 3) + (x**3 - 2*x)*(2*x - 4)

# 점 검증
assert abs(f(1) - (-6)) < 1e-10, 'f(1) != -6'
assert abs(g(1) - 6) < 1e-10, 'g(1) != 6'

slope_l = f_prime(1)  # -2
slope_m = g_prime(1)  # -4

# 접선 l: y = slope_l*(x-1) + (-6)
def l_line(x):
    return slope_l*(x - 1) + (-6)

# 접선 m: y = slope_m*(x-1) + 6
def m_line(x):
    return slope_m*(x - 1) + 6

y_l0 = l_line(0)   # y절편
y_m0 = m_line(0)   # y절편

# 교점 x좌표
x_int = (y_m0 - y_l0) / (slope_l - slope_m)
y_int = l_line(x_int)

# 삼각형 넓이
base = abs(y_m0 - y_l0)
height = abs(x_int)
area = 0.5 * base * height

if abs(area - 49) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}')
