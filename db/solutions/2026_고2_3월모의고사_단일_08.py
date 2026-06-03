import sympy as sp
from numpy import linspace

# 원래 함수 정의
def f(x, a, b):
    return a / (x - 1) + b

a, b = 4, 3
x_vals = linspace(3, 5, 100)
f_vals = [f(x, a, b) for x in x_vals]

max_val = max(f_vals)
min_val = min(f_vals)

print(f'Maximum: {max_val}, Expected: 5')
print(f'Minimum: {min_val}, Expected: 4')
print(f'f(3) = {f(3, a, b)}')
print(f'f(5) = {f(5, a, b)}')

if abs(max_val - 5) < 0.001 and abs(min_val - 4) < 0.001 and f(3, a, b) == 5 and f(5, a, b) == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')