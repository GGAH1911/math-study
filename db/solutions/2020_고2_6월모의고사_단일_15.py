import numpy as np
# y=tanπx ([0,2]) 와 y=-10/3 x+n 이 서로 다른 3점에서 만나는 자연수 n 최댓값? (⑤=6)
CANDIDATE = 6
def count(n):
    c = 0
    for lo, hi in [(0, 0.5), (0.5, 1.5), (1.5, 2)]:
        xs = np.linspace(lo+1e-6, hi-1e-6, 300000)
        d = np.tan(np.pi*xs) - (-10/3*xs + n)
        c += np.sum(np.diff(np.sign(d)) != 0)
    return c
mx = max(n for n in range(1, 30) if count(n) == 3)
print('VERIFY_PASS' if mx == CANDIDATE else 'VERIFY_FAIL')
