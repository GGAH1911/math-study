import numpy as np

def S(t):
    if abs(t) < 1e-15:
        return 0.0
    return 0.5 * abs(t) * (2.0**t) * abs(2.0**t - 1.0)

# ㄱ: S(1) == 1
if abs(S(1) - 1.0) > 1e-10:
    print('VERIFY_FAIL: ㄱ')
    exit()

# ㄴ: S(2) == 64 * S(-2)
if abs(S(2) - 64 * S(-2)) > 1e-10:
    print('VERIFY_FAIL: ㄴ')
    exit()

# ㄷ: S(t)/S(-t) = 2^(3t) strictly increasing for t > 0
def ratio(t):
    return S(t) / S(-t)

t_vals = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0]
ratios = [ratio(t) for t in t_vals]
expected = [2**(3*t) for t in t_vals]

for i, (r, e) in enumerate(zip(ratios, expected)):
    if abs(r - e) > 1e-8:
        print(f'VERIFY_FAIL: ratio mismatch at t={t_vals[i]}, got {r}, expected {e}')
        exit()

if not all(ratios[i] < ratios[i+1] for i in range(len(ratios)-1)):
    print('VERIFY_FAIL: ㄷ not increasing')
    exit()

print('VERIFY_PASS')