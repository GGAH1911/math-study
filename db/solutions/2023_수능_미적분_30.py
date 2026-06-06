import numpy as np
from scipy.optimize import fsolve
import math

# f(x) = (5/9)x^3 - (5/2)x^2 + 8
def f(x):
    return (5/9)*x**3 - (5/2)*x**2 + 8

def h(x):
    return np.exp(np.sin(np.pi*f(x))) - 1

# 조건 검증
# (가) h(0) = 0
h_0 = h(0)
print(f'h(0) = {h_0:.10f}')
assert abs(h_0) < 1e-10, 'VERIFY_FAIL'

# f'(0) = 0, f'(3) = 0
def f_prime(x):
    return (5/3)*x**2 - 5*x

print(f'f\'(0) = {f_prime(0)}')
print(f'f\'(3) = {f_prime(3)}')
assert abs(f_prime(0)) < 1e-10 and abs(f_prime(3)) < 1e-10, 'VERIFY_FAIL'

# f(3) = 1/2
f_3 = f(3)
print(f'f(3) = {f_3}')
assert abs(f_3 - 0.5) < 1e-10, 'VERIFY_FAIL'

# (나) (0,3)에서 sin(π*f(x)) = ln(2)의 근이 7개
ln2 = np.log(2)
root_count = 0
for start in np.linspace(0.01, 2.99, 100):
    try:
        root = fsolve(lambda x: np.sin(np.pi*f(x)) - ln2, start, full_output=True)
        if root[2] == 1 and 0 < root[0][0] < 3:
            if root_count == 0 or abs(root[0][0] - roots[-1]) > 0.01:
                roots = [root[0][0]] if root_count == 0 else roots + [root[0][0]]
                root_count += 1
    except:
        pass

# 더 정확한 근의 개수 세기
roots = []
for u_start in np.linspace(0.51, 7.99, 300):
    try:
        sol = fsolve(lambda x: np.sin(np.pi*x) - ln2, u_start, full_output=True)
        if sol[2] == 1 and 0.5 < sol[0][0] < 8:
            is_new = True
            for existing in roots:
                if abs(sol[0][0] - existing) < 0.001:
                    is_new = False
                    break
            if is_new:
                roots.append(sol[0][0])
    except:
        pass

roots.sort()
print(f'Number of roots in (0.5, 8) where sin(π*u) = ln(2): {len(roots)}')
for i, r in enumerate(roots):
    print(f'  Root {i+1}: u ≈ {r:.4f}')

assert len(roots) == 7, f'VERIFY_FAIL: expected 7 roots, got {len(roots)}'

# f(2) = 22/9
f_2 = f(2)
print(f'f(2) = {f_2} = {f_2.as_integer_ratio()[0]}/{f_2.as_integer_ratio()[1]}')
print(f'f(2) = 22/9 = {22/9}')
assert abs(f_2 - 22/9) < 1e-10, 'VERIFY_FAIL'

print('VERIFY_PASS')