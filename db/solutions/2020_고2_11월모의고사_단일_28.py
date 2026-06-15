import sympy as sp
import numpy as np

CANDIDATE = 15

# 기호 계산
t = sp.Symbol('t', real=True)
p = sp.sqrt(2 / (1 + t**2))

S_t = sp.Rational(1, 2) * (1 - t) * (p - t)

# t=1에서의 극한값 계산
limit_k = sp.limit(S_t / (1 - t)**2, t, 1)
print(f'Limit of S(t)/(1-t)^2 as t→1: {limit_k}')

k_value = float(limit_k)
answer_value = 20 * k_value
print(f'20k = {answer_value}')

# 수치 검증
print('\nNumerical verification:')
for t_val in [0.9, 0.99, 0.999, 0.9999]:
    p_val = float(np.sqrt(2 / (1 + t_val**2)))
    S_val = 0.5 * (1 - t_val) * (p_val - t_val)
    ratio = S_val / (1 - t_val)**2
    print(f't={t_val}: S(t)/(1-t)^2 = {ratio:.6f}')

if abs(answer_value - CANDIDATE) < 0.001:
    print(f'\nVERIFY_PASS')
else:
    print(f'\nVERIFY_FAIL')