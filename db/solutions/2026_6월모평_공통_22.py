import numpy as np
from scipy.optimize import fsolve

# s + 2^s = 35/3을 풀어 s를 구함
def equation(s):
    return s + 2**s - 35/3

s_val = fsolve(equation, 3.1)[0]
k_val = 2**s_val

# 검증: 삼각형 넓이 계산
u_val = s_val  # u = s인 경우
x_A = s_val - 1
y_A = 2**s_val
x_B = u_val + 2
y_B = 2**u_val - 3

# 넓이 = (1/2)|x_A*y_B - y_A*x_B|
area = 0.5 * abs(x_A * y_B - y_A * x_B)

# 조건 확인: 2^u + u = s + 2^s
condition_check = abs(2**u_val + u_val - (s_val + 2**s_val)) < 1e-6

# k + log_2(k) = 35/3 확인
log_sum = k_val + s_val
target = 35/3
sum_check = abs(log_sum - target) < 1e-6

# gcd(35, 3) = 1 확인
from math import gcd
coprime_check = gcd(35, 3) == 1

if abs(area - 16) < 0.1 and condition_check and sum_check and coprime_check:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}, u==s: {condition_check}, sum={log_sum}, target={target}, coprime: {coprime_check}')