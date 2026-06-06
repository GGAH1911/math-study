import numpy as np
from scipy.optimize import fsolve

a, b = 2, -3/5

# 조건 (가) 검증: sin(2πx) = -b의 해의 합
def eq_ga(x):
    return np.sin(2*np.pi*x) + b

# 해 찾기
roots_ga = []
for init in [0.1, 0.4]:
    root = fsolve(eq_ga, init)[0]
    if abs(root) <= 0.5 and abs(eq_ga(root)) < 1e-9:
        roots_ga.append(root)

roots_ga = sorted(list(set([round(r, 10) for r in roots_ga])))
sum_ga = sum(roots_ga)

# 조건 (나) 검증: |sin(2πx) + b| = 2/5의 해의 합
def eq_na_pos(x):
    return np.sin(2*np.pi*x) + b - 2/5

def eq_na_neg(x):
    return np.sin(2*np.pi*x) + b + 2/5

roots_na = []
# 첫 번째 식
for init in [0.25]:
    try:
        root = fsolve(eq_na_pos, init)[0]
        if abs(root) <= 0.5 and abs(eq_na_pos(root)) < 1e-9:
            roots_na.append(root)
    except:
        pass

# 두 번째 식
for init in [0.05, 0.45]:
    try:
        root = fsolve(eq_na_neg, init)[0]
        if abs(root) <= 0.5 and abs(eq_na_neg(root)) < 1e-9:
            roots_na.append(root)
    except:
        pass

roots_na = sorted(list(set([round(r, 10) for r in roots_na])))
sum_na = sum(roots_na)

# 검증
verify_ga = abs(sum_ga - 0.5) < 1e-9
verify_na = abs(sum_na - 0.75) < 1e-9

if verify_ga and verify_na:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')