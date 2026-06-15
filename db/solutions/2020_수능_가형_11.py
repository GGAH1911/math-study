import sympy as sp
from sympy import sin, cos, diff, symbols, solve

x = symbols('x', real=True)

def check_inflection_point_exists(a_val):
    y = a_val * x**2 - 2*sin(2*x)
    y_prime = diff(y, x)
    y_double_prime = diff(y_prime, x)
    
    # y'' = 0의 해: 2*a + 8*sin(2x) = 0
    # sin(2x) = -a/4
    
    if abs(-a_val/4) > 1:
        return False
    
    # cos(2x) = 0인지 확인
    # sin(2x) = -a/4일 때 cos^2(2x) = 1 - a^2/16
    cos_squared = 1 - a_val**2/16
    
    if abs(cos_squared) < 1e-10:  # cos(2x) = 0
        return False
    
    return True

count = 0
for a in range(-10, 11):
    if check_inflection_point_exists(a):
        count += 1

if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')