import numpy as np
from scipy import integrate

CANDIDATE = 93

# f(1) = -1, f(3) = 5로 결정됨
f_1 = -1
f_3 = 5

# f'(u) = -π sin(πx(u)) + 5(u-1)
# where x(u) = (-1 + sqrt(4u-3))/2

def x_of_u(u):
    return (-1 + np.sqrt(4*u - 3)) / 2

def f_prime(u):
    if u < 0.75:
        return None
    x = x_of_u(u)
    return -np.pi * np.sin(np.pi * x) + 5*(u - 1)

# 검증: 주어진 함수방정식 확인
def verify_equation(x_val):
    u = x_val**2 + x_val + 1
    lhs = f_prime(u)
    rhs = np.pi * f_1 * np.sin(np.pi * x_val) + f_3 * x_val + 5 * x_val**2
    return np.isclose(lhs, rhs)

# 특정 점에서 검증
assert verify_equation(0), "x=0 검증 실패"
assert verify_equation(1), "x=1 검증 실패"
assert verify_equation(2), "x=2 검증 실패"
assert verify_equation(0.5), "x=0.5 검증 실패"

# f 함수 계산 (적분)
def f(u):
    if u == 1:
        return f_1
    elif u == 3:
        return f_3
    elif u == 7:
        # f(u) = ∫f'(t)dt + f(1)
        def integrand(x):
            return np.sin(np.pi*x) * (2*x + 1)
        x_lower = 0
        x_upper = (-1 + np.sqrt(4*u - 3)) / 2
        integral, _ = integrate.quad(integrand, x_lower, x_upper)
        return -np.pi * integral + 5*(u-1)**2/2 + f_1

f_7 = f(7)

if np.isclose(f_7, CANDIDATE):
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: computed f(7)={f_7}, expected {CANDIDATE}")