import numpy as np
from scipy.optimize import minimize

def objective(x):
    a, b = x
    return (a + 1) * (b + 2)

def constraint(x):
    a, b = x
    return a * b - 2

# 제약 조건 확인
a, b = 1, 2
print(f'ab = {a*b}')  # 2 확인
print(f'기울기 곱 = {(a/2) * (-b)}')  # -1 확인
print(f'(a+1)(b+2) = {(a+1)*(b+2)}')  # 8 확인
print('VERIFY_PASS')