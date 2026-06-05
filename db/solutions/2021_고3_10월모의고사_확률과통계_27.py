import numpy as np

# 두 PDF의 교점 a 계산 (sigma 동일 → 지수부 비교)
# (a-8)^2 = (a-12)^2 → 8a = 80 → a = 10
a = 10.0
assert abs(a - 10.0) < 1e-9, 'a 계산 오류'

# 표준정규분포 표 값 (문제에 주어진 값)
table = {0.5: 0.1915, 1.0: 0.3413, 1.5: 0.4332, 2.0: 0.4772}

# Y ~ N(12, 4), P(8 <= Y <= 10) 계산
# Z = (Y-12)/2
z_low = (8 - 12) / 2   # = -2.0
z_high = (10 - 12) / 2  # = -1.0

# P(-2 <= Z <= -1) = P(1 <= Z <= 2) [대칭성]
# = P(0<=Z<=2) - P(0<=Z<=1)
prob = table[abs(z_low)] - table[abs(z_high)]  # 0.4772 - 0.3413

my_answer = 0.1359

if abs(prob - my_answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed={prob}, expected={my_answer}')
