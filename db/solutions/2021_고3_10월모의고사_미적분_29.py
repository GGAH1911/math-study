import numpy as np
from fractions import Fraction

# 후보 a 값: a = 2k/3, k = 1..6
a_values = [Fraction(2*k, 3) for k in range(1, 7)]

# numpy 버전 무관 사다리꼴 적분
def trap(y, x):
    return 0.5 * float(np.sum((y[1:] + y[:-1]) * (x[1:] - x[:-1])))

# 조건 (나) 수치 검증: 원래 식 그대로 적분
def check_na(a_float, ts, atol=5e-3):
    N = 200001
    xs = np.linspace(0.0, 3.0 * np.pi, N)
    fx = np.sin(a_float * xs)
    for t in ts:
        I_plus = trap(np.abs(fx + t), xs)
        I_minus = trap(np.abs(fx - t), xs)
        if abs(I_plus - I_minus) > atol:
            return False
    return True

# 조건 (가) 수치 검증: 원래 식 적분 후 1/2 비교
def check_ga(a_float):
    N = 100001
    xs = np.linspace(0.0, np.pi / a_float, N)
    fx = np.sin(a_float * xs)
    val = trap(fx, xs)
    return val >= 0.5 - 1e-6

ts_grid = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
all_candidates_ok = True
for a in a_values:
    af = float(a)
    if not check_ga(af):
        all_candidates_ok = False
        break
    if not check_na(af, ts_grid):
        all_candidates_ok = False
        break

# 비-후보 a 가 (나)를 위반해야 함
non_cand_1_fails = not check_na(1.0, [0.5])
non_cand_05_fails = not check_na(0.5, [0.5])
non_cand_15_fails = not check_na(1.5, [0.5])

# a > 4 는 (가) 위반
ga_a5_fails = not check_ga(5.0)

# 합 = 14
total = sum(float(a) for a in a_values)
sum_ok = abs(total - 14.0) < 1e-9

if (all_candidates_ok and non_cand_1_fails and non_cand_05_fails
    and non_cand_15_fails and ga_a5_fails and sum_ok):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
