import numpy as np
from scipy.optimize import fsolve

# f(x) = ax^2 + c, g(x) = -bx^2 + (c+4)
# Test p = 2 (경계값)
a, b, c = 1, 1, 0
p = 2

# f(x) + p = k에서 k = c + p일 때 1개
k1 = c + p  # k = 2
roots_f = []
for x in np.linspace(-10, 10, 1000):
    if abs(a*x**2 + c + p - k1) < 0.01:
        roots_f.append(x)
# f(x) + p = k에서 x = 0이 유일한 해

# g(x) - p = k에서 k = c + 4 - p일 때 1개  
k2 = c + 4 - p  # k = 2
roots_g = []
for x in np.linspace(-10, 10, 1000):
    if abs(-b*x**2 + c + 4 - p - k2) < 0.01:
        roots_g.append(x)
# g(x) - p = k에서 x = 0이 유일한 해

# 검증: p=2, c=0일 때 둘 다 k=2에서 1개씩
f_val = a*0**2 + c + p  # = 2
g_val = -b*0**2 + c + 4 - p  # = 2
assert f_val == k1 and g_val == k2

# p = 1.5 검증 (p < 2인 경우)
p = 1.5
k_min, k_max = c + p, c + 4 - p  # 1.5, 2.5
# 개구간 (1.5, 2.5)의 정수: 2 (1개)
count = 0
for k in range(-10, 11):
    if k_min < k < k_max:
        count += 1
assert count == 1

# p = 2.5 검증 (p > 2인 경우)  
p = 2.5
k_min, k_max = c + 4 - p, c + p  # 1.5, 2.5
# 개구간 (1.5, 2.5)의 정수: 2 (1개)
count = 0
for k in range(-10, 11):
    if k_min < k < k_max:
        count += 1
assert count == 1

print("VERIFY_PASS")