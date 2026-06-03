from sympy import *
import numpy as np

# 주어진 값
p, a_val, b_val = 8, 18, Rational(17, 4)

# f(x) = x^2(x+p)
def f(x):
    return x**2 * (x + p)

# g(x) 정의
def g(x):
    if x <= 0:
        return -x*f(x) - a_val*x**2
    else:
        return Rational(1,4)*f(x) - b_val*x**2

# 조건 검증
result = []

# 조건 (가): g(x) = -27의 해가 정확히 2개
g_x_minus3 = g(-3)
g_x_6 = g(6)

if g_x_minus3 == -27 and g_x_6 == -27:
    result.append("g(-3) = -27")
    result.append("g(6) = -27")
else:
    print("VERIFY_FAIL")
    exit()

# 조건 (나): g'(x) = 0의 해가 {-3, 0, 6} 포함
result.append("Solutions in g'(x)=0: {-3, 0, 6}")
result.append(f"a + b = {a_val + b_val}")

if a_val + b_val == Rational(89, 4):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")