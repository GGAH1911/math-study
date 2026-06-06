import numpy as np
from scipy.optimize import minimize_scalar

def f(x):
    return 5 * np.sin(x) + 1

# sin(x)의 최댓값 1을 직접 사용
max_val = 5 * 1 + 1
print(f'Expected maximum: {max_val}')

# 수치적으로 최댓값 확인
result = minimize_scalar(lambda x: -f(x), bounds=(0, 2*np.pi), method='bounded')
max_numerical = -result.fun

print(f'Numerical maximum: {max_numerical}')
print(f'Answer to verify: 6')

if abs(max_val - 6) < 1e-9 and abs(max_numerical - 6) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')