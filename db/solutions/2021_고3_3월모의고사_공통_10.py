import sympy as sp
import numpy as np

# 정의
n_val = 1
f_1 = -1/n_val

n_val = 2
g_2 = (1/2) * (n_val**3 + n_val**5)

r = 0
for n in range(1, 9):
    S_n = (1/2) * (n**3 + n**5)
    r += S_n / (n**3)

result = f_1 + g_2 + r

# 검증
print(f'f(1) = {f_1}')
print(f'g(2) = {g_2}')
print(f'r = {r}')
print(f'f(1) + g(2) + r = {result}')

if abs(result - 125) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')