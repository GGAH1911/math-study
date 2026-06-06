import numpy as np
from scipy import integrate
import sympy as sp

# 함수 정의
def f(x):
    return x**2 - 8*x + 20

def f_prime(x):
    return 2*x - 8

def g(x):
    return np.log(x**2 - 6*x + 13)

# 조건 (나) 검증: g(4) = ln 5
g_4 = np.log(16 - 24 + 13)
expected_g4 = np.log(5)
print(f'g(4) = {g_4}, ln(5) = {expected_g4}, 일치: {np.isclose(g_4, expected_g4)}')

# 적분 검증
def integrand(x):
    return (f_prime(x) + 2) * g(x)

result, _ = integrate.quad(integrand, 3, 5)
expected = -4 + 16*np.log(2)

print(f'적분값: {result}')
print(f'기댓값: {expected}')
print(f'일치: {np.isclose(result, expected)}')

if np.isclose(result, expected):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')