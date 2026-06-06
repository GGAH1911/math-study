import numpy as np
from scipy.optimize import fsolve

# a = 9
a = 9

# 첫 번째 함수의 주기
period1 = 2 * np.pi / (2/3)
print(f'Period of cos(2x/3): {period1}')

# 두 번째 함수의 주기  
period2 = np.pi / (3/a)
print(f'Period of tan(3x/a) with a=9: {period2}')

# 주기가 같은지 확인
if np.isclose(period1, period2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')