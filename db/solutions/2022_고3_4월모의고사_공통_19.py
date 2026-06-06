import numpy as np
from scipy.optimize import minimize_scalar

# 원래 함수 g(x) = x^4 - 4x^3 + 16x
def g(x):
    return x**4 - 4*x**3 + 16*x

# g(x)의 최솟값 찾기
result = minimize_scalar(g, bounds=(-10, 10), method='bounded')
g_min = result.fun
print(f'g(x)의 최솟값: {g_min:.6f}')

# 정확한 임계점 계산
g_at_minus1 = (-1)**4 - 4*(-1)**3 + 16*(-1)
print(f'g(-1) = {g_at_minus1}')

# a = 11일 때 f(x) = x^4 - 4x^3 + 16x + 11이 모든 x에서 >= 0인지 확인
def f(x):
    return x**4 - 4*x**3 + 16*x + 11

result_f = minimize_scalar(f, bounds=(-10, 10), method='bounded')
f_min = result_f.fun
print(f'a=11일 때 f(x)의 최솟값: {f_min:.6f}')

# f(-1) = 0인지 확인
f_minus1 = (-1)**4 - 4*(-1)**3 + 16*(-1) + 11
print(f'f(-1) = {f_minus1}')

if f_min >= -1e-9 and f_minus1 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')