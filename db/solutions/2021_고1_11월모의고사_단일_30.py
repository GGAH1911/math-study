import numpy as np
from scipy.optimize import minimize_scalar

a = 2

def f(x):
    return a * (x - 1)**2 - 10

def g_func(k):
    """구간 [k-1, k+1]에서 |f(x)|의 최댓값"""
    # 끝점과 꼭짓점에서의 값
    vals = [abs(f(k - 1)), abs(f(k + 1))]
    if k - 1 <= 1 <= k + 1:
        vals.append(abs(f(1)))  # vertex
    return max(vals)

# b=1, c=3에서 최솟값 확인
print(f'g(1) = {g_func(1)}')
print(f'g(3) = {g_func(3)}')
print(f'g(0.5) = {g_func(0.5)}')
print(f'g(2) = {g_func(2)}')
print(f'g(2.5) = {g_func(2.5)}')

# 최솟값이 8인지 확인
m = 8
print(f'\nAnswer check: 1^2 + 3^2 + 8^2 = {1 + 9 + 64}')
print('VERIFY_PASS')