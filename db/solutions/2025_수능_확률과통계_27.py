import numpy as np

# 모집단
pop = np.array([1, 3, 5, 7, 9])

# 모집단 분산 (모분산)
sigma2 = np.var(pop)  # 분모 N=5
print(f'sigma^2 = {sigma2}')  # 8.0

# 표본 크기
n = 3

# 표본평균의 분산
var_Xbar = sigma2 / n
print(f'V(Xbar) = {var_Xbar}')  # 8/3

# a 값
a = 3

# V(a*Xbar + 6) = a^2 * V(Xbar)
result = a**2 * var_Xbar
print(f'V(a*Xbar + 6) = {result}')  # should be 24

if abs(result - 24) < 1e-9 and a > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
