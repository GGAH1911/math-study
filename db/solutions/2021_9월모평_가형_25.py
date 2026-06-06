import numpy as np
from scipy import integrate

# 원래 함수 f(x) = x^4
def f(x):
    return x**4

# 정적분 계산
result, _ = integrate.quad(f, 1, 3)
print(f'적분값: {result}')

# 해석적 계산
analytical = (3**5 - 1**5) / 5
print(f'해석적값: {analytical}')

# a = 242/5
a = analytical
five_a = 5 * a
print(f'5a = {five_a}')

# 검증: 5a = 242인지 확인
if abs(five_a - 242) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')