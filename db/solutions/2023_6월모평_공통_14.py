import numpy as np

def f(x, a):
    if x < 0:
        return -3*x**2 - 2*a*x
    else:
        return 3*x**2 + 2*a*x

def g(x, a):
    return x**3 + a*x**2

all_pass = True

# ㄱ: f(0)=0 for all a
for a_val in [-2.0, -1.0, 0.0, 1.0, 2.0]:
    if abs(f(0, a_val)) > 1e-12:
        all_pass = False

# g(0)=0 확인
for a_val in [-1.0, 0.0, 1.0]:
    if abs(g(0, a_val)) > 1e-12:
        all_pass = False

# ㄷ: 2 < f(1) < 4 인 경우 (즉 -1/2 < a < 1/2) f(x)=x 실근 정확히 3개
for a_val in np.linspace(-0.499, 0.499, 300):
    f1 = f(1, a_val)
    if not (2 < f1 < 4):
        all_pass = False
        break
    r1 = -(2*a_val + 1) / 3  # 음수 근
    r2 = 0.0
    r3 = (1 - 2*a_val) / 3   # 양수 근
    if not (r1 < 0 < r3):
        all_pass = False
        break
    for r in [r1, r2, r3]:
        if abs(f(r, a_val) - r) > 1e-8:
            all_pass = False
            break

# ㄴ 반례 확인: a=0이면 극댓값 없음
a_val = 0.0
xs = np.linspace(-5, 5, 100000)
fs = np.array([f(xi, a_val) for xi in xs])
has_local_max = any(fs[i] > fs[i-1] and fs[i] > fs[i+1] for i in range(1, len(fs)-1))
if has_local_max:
    all_pass = False  # 반례가 없으면 ㄴ이 틀리지 않은 게 돼서 문제

print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')