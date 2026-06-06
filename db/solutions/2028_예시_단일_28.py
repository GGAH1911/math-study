import numpy as np
from scipy.optimize import fsolve

# 주어진 원래 함수
def f(t):
    return t * (t - 1)**2 * (t - 2)

# 구한 답: a = -1, k = sqrt(2)/2
a = -1
k = np.sqrt(2) / 2

# 조건 검증
# 1. g(-k) = g(k) 확인
g_k = f(k - a)
g_neg_k = f(-k - a)
print(f"g(k) = {g_k}")
print(f"g(-k) = {g_neg_k}")
print(f"g(-k) == g(k): {np.isclose(g_k, g_neg_k)}")

# 2. f'(k+1) = 0 확인 (g'(k) = 0)
def f_prime(t):
    return 2 * (t - 1) * (2*t**2 - 4*t + 1)

f_prime_val = f_prime(k + 1)
print(f"\nf'(k+1) = {f_prime_val}")
print(f"f'(k+1) ≈ 0: {np.isclose(f_prime_val, 0)}")

# 3. f'(1-k) = 0 확인 (g'(-k) = 0)
f_prime_val2 = f_prime(1 - k)
print(f"f'(1-k) = {f_prime_val2}")
print(f"f'(1-k) ≈ 0: {np.isclose(f_prime_val2, 0)}")

# 최종 답
answer = a + 20 * k**2
print(f"\na + 20k² = {answer}")
print(f"Answer = {int(round(answer))}")

if int(round(answer)) == 9:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")