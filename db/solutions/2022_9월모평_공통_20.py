import numpy as np
from scipy.optimize import fsolve

def f(x):
    return 0.5*x**3 - 4.5*x**2 + 10*x

def equation(x, k):
    return f(x) + abs(f(x) + x) - (6*x + k)

k = 3  # 예: k = 3 (1-6 범위 내)
roots = []

# 근을 광범위에서 찾기
for start in np.linspace(-5, 5, 30):
    try:
        root = fsolve(lambda x: equation(x, k), start, full_output=True)
        if root[2] == 1:  # 수렴 확인
            r = root[0][0]
            if abs(equation(r, k)) < 1e-10:
                # 중복 제거
                is_new = True
                for existing_root in roots:
                    if abs(r - existing_root) < 1e-6:
                        is_new = False
                        break
                if is_new:
                    roots.append(r)
    except:
        pass

roots.sort()
print(f'k={k}: {len(roots)} 근')
for r in roots:
    print(f'  x={r:.6f}, 검증: {equation(r, k):.2e}')

# 4개 근을 가지는 k 확인
result = []
for k_test in range(1, 7):
    roots_test = []
    for start in np.linspace(-10, 10, 50):
        try:
            root = fsolve(lambda x: equation(x, k_test), start, full_output=True)
            if root[2] == 1:
                r = root[0][0]
                if abs(equation(r, k_test)) < 1e-10:
                    is_new = True
                    for existing_root in roots_test:
                        if abs(r - existing_root) < 1e-6:
                            is_new = False
                            break
                    if is_new:
                        roots_test.append(r)
        except:
            pass
    if len(roots_test) == 4:
        result.append(k_test)

print(f'\n4개 근을 가지는 정수 k: {result}')
print(f'합: {sum(result)}')
if sum(result) == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')