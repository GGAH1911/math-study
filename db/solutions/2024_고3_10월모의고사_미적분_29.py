import numpy as np
from scipy.optimize import fsolve

e = np.e
a = e - 2

# 교점 방정식: x*tan(theta) = exp(x/a) - 2
def equation(x, theta):
    return x * np.tan(theta) - np.exp(x/a) + 2

# f(theta) 함수: 교점의 x좌표
def f_func(theta):
    def eq(x):
        return equation(x, theta)
    sol = fsolve(eq, 1.0)[0]
    return sol

# f(pi/4) = a 확인
theta_pi4 = np.pi / 4
f_pi4 = f_func(theta_pi4)
if abs(f_pi4 - a) > 1e-6:
    print('VERIFY_FAIL')
    exit()

# f'(pi/4) 수치 미분
h = 1e-8
f_prime_pi4_numerical = (f_func(theta_pi4 + h) - f_pi4) / h
f_prime_pi4_theoretical = (e - 2)**2

if abs(f_prime_pi4_numerical - f_prime_pi4_theoretical) > 1e-4:
    print('VERIFY_FAIL')
    exit()

# sqrt(f'(pi/4)) = e - 2 확인
sqrt_val = np.sqrt(f_prime_pi4_theoretical)
if abs(sqrt_val - (e - 2)) > 1e-10:
    print('VERIFY_FAIL')
    exit()

# p = 1, q = -2 확인
p, q = 1, -2
if abs(p * e + q - (e - 2)) > 1e-10:
    print('VERIFY_FAIL')
    exit()

if p**2 + q**2 != 5:
    print('VERIFY_FAIL')
    exit()

print('VERIFY_PASS')