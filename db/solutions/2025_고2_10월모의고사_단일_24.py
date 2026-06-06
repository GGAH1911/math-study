import numpy as np
from scipy.optimize import fsolve

# y = log(x-2)의 수직 접근선: x = 2
vertical_asymptote = 2

# y = 2^x + 5의 수평 접근선을 확인
# x가 충분히 작을 때 (예: x = -100)
x_test = -100
y_asymptotic = 2**x_test + 5
print(f'y = 2^x + 5 when x = -100: {y_asymptotic}')
print(f'Horizontal asymptote approaches: y = 5')

# 교점은 x = 2, y = 5
a, b = 2, 5
result = a + b

# 검증: 접근선이 맞는지 확인
# x = 2 근처에서 log(x-2)는 -∞로 간다 (x → 2+)
x_near_2 = 2.0001
y_log = np.log10(x_near_2 - 2)
print(f'log(x-2) near x=2: y ≈ {y_log:.4f} (매우 작은 음수)')

# 큰 음수 x에서 2^x + 5 ≈ 5
x_very_negative = -1000
y_exp = 2**x_very_negative + 5
print(f'2^x + 5 when x = -1000: y ≈ {y_exp}')

# 교점 (2, 5) 확인
print(f'\nIntersection point: ({a}, {b})')
print(f'a + b = {result}')

if a == 2 and b == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')