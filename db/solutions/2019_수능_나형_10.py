from scipy import integrate
import numpy as np

# pdf 정의
def pdf(x):
    if x < 1/3:
        return (3/4) / (1/3) * x  # 0부터 1/3까지 직선
    elif x <= 1:
        return 3/4
    elif x <= 2:
        return (3/4) * (2 - x) / (2 - 1)  # 1부터 2까지 직선
    else:
        return 0

# 전체 확률 확인
total_prob, _ = integrate.quad(pdf, 0, 2)
print(f'Total probability: {total_prob}')

# P(1/3 <= X <= 1) 계산
prob, _ = integrate.quad(pdf, 1/3, 1)
print(f'P(1/3 <= X <= 1) = {prob}')

if abs(prob - 0.5) < 1e-10 and abs(total_prob - 1.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')