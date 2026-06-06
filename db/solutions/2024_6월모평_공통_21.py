import numpy as np
from scipy.optimize import fsolve
import math

# 두 곡선의 교점 조건: t - log_2(x) = 2^(x-t)
def find_f(t):
    def equation(x):
        return t - np.log2(x) - 2**(x - t)
    # x > 0 범위에서 해를 찾음
    x_initial = t + 0.5  # 초기값
    sol = fsolve(equation, x_initial)[0]
    return sol

# ㄱ 검증: f(1) = 1, f(2) = 2
f1 = find_f(1.0)
f2 = find_f(2.0)
print(f"f(1) ≈ {f1:.6f}, expected 1")
print(f"f(2) ≈ {f2:.6f}, expected 2")

# 검증: 교점이 정말 두 곡선의 교점인지 확인
def verify_intersection(t, x):
    y1 = t - np.log2(x)
    y2 = 2**(x - t)
    return abs(y1 - y2) < 1e-9

check1 = verify_intersection(1.0, f1)
check2 = verify_intersection(2.0, f2)
print(f"Intersection verified for t=1: {check1}")
print(f"Intersection verified for t=2: {check2}")

# ㄴ 검증: f(t)가 증가함수인가
t_vals = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
f_vals = [find_f(t) for t in t_vals]
is_increasing = all(f_vals[i+1] > f_vals[i] for i in range(len(f_vals)-1))
print(f"\nf(t) is increasing: {is_increasing}")
for t, f in zip(t_vals, f_vals):
    print(f"  f({t}) ≈ {f:.4f}")

# ㄷ 검증: 모든 양의 실수 t에 대해 f(t) >= t인가
t_test = np.linspace(0.5, 3, 20)
f_test = [find_f(t) for t in t_test]
violations = [t for t, f in zip(t_test, f_test) if f < t - 1e-6]
print(f"\nt values where f(t) < t: {violations}")
print(f"ㄷ is false: {len(violations) > 0}")

# 답 검증
print(f"\nA=100 (ㄱ true), B=10 (ㄴ true), C=0 (ㄷ false)")
print(f"A + B + C = 110")
if len(violations) > 0 and check1 and check2 and is_increasing:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")