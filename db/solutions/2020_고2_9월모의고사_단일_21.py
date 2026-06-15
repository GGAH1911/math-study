import numpy as np
# f 짝·주기4 (2→3→1→3→2). a_n=#(y=log_{2^n}(x+2n) ∩ y=f). a_1+a_2+a_3? (②=535)
# |f-log| 의 극솟값(≈0) 으로 교차·접점 모두 카운트.
CANDIDATE = 535
def f(x):
    t = np.mod(x, 4)
    t = np.where(t > 2, 4 - t, t)
    return np.where(t < 1, t + 2, -2*t + 5)
def a(n):
    base = 2**n
    hi = base**3 - 2*n
    pts = min(60_000_000, int((hi + 2*n) * 8000) + 200000)
    xs = np.linspace(-2*n + 1e-7, hi + 1e-3, pts)
    d = np.abs(f(xs) - np.log(xs + 2*n)/np.log(base))
    loc = (d[1:-1] <= d[:-2]) & (d[1:-1] < d[2:]) & (d[1:-1] < 1e-2)
    return int(np.sum(loc))
print('VERIFY_PASS' if a(1)+a(2)+a(3) == CANDIDATE else 'VERIFY_FAIL')
