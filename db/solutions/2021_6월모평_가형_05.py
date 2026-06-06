import sympy as sp
import numpy as np

# 조건을 만족하는 예시: a_n = 60/(pi^2 * n)
# sum(a_n/n) = sum(60/(pi^2 * n^2)) = 60/pi^2 * pi^2/6 = 10 ✓

# 일반적 증명: lim(a_n/n) = 0 이면
# lim(a_n + 2*a_n^2 + 3*n^2)/(a_n^2 + n^2)
# = lim[(a_n/n^2) + 2(a_n/n)^2 + 3] / [(a_n/n)^2 + 1]
# = [0 + 0 + 3] / [0 + 1] = 3

# 수치적 검증: a_n = 60/(pi^2 * n) 대입
pi = np.pi
n_large = 1000
a_n = 60 / (pi**2 * n_large)

numerator = a_n + 2*a_n**2 + 3*n_large**2
denominator = a_n**2 + n_large**2
result = numerator / denominator

if abs(result - 3) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')