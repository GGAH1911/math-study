import sympy as sp
from scipy.integrate import quad
import numpy as np

# 정의: f(x) = (3/4)x, a = 3/2
def f(x):
    return (3/4) * x

def integrand(t, x_upper):
    abs_f_t = abs(f(t))
    return (t**2 - 4) * (abs_f_t - 3/2)

# g(x) 수치적으로 계산
def g(x):
    if x == 0:
        return 0
    result, _ = quad(integrand, 0, x, args=(x,))
    return result

# 검증
g_0 = 0  # g(0) = 0 (정의)
g_2, _ = quad(integrand, 0, 2, args=(2,))
g_minus_4, _ = quad(integrand, 0, -4, args=(-4,))

result = g_0 - g_minus_4

print(f"g(2) = {g_2:.6f} (expected: 5.0)")
print(f"g(0) = {g_0}")
print(f"g(-4) = {g_minus_4:.6f}")
print(f"g(0) - g(-4) = {result:.1f}")

if abs(g_2 - 5.0) < 0.01 and abs(result - 16.0) < 0.01:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")