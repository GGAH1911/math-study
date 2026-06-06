import numpy as np
from scipy.optimize import fsolve

k = 3

def equation(x):
    return x**3 + 3*x**2 - k

# 서로 다른 근을 찾기 위해 여러 초기값 사용
roots = []
initial_values = [-3, -1, 1]
for iv in initial_values:
    root = fsolve(equation, iv)[0]
    # 이미 찾은 근과 중복 확인
    is_duplicate = any(abs(root - r) < 1e-8 for r in roots)
    if not is_duplicate and abs(equation(root)) < 1e-8:
        roots.append(root)

if len(roots) == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')