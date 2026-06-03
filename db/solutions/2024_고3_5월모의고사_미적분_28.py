import numpy as np

tan_b_answer = 3
# 조건 (가)에서 b/2 in (0, pi/2)이므로 b in (0, pi/2), b = arctan(3)
b_val = np.arctan(tan_b_answer)
a_val = 1.0/np.tan(b_val/2.0)
assert a_val > 0

def f(x):
    return a_val*np.sin(x) - np.cos(x)
def g(x):
    return np.exp(2*x - b_val) - 1
def fp(x):
    return a_val*np.cos(x) + np.sin(x)
def gp(x):
    return 2*np.exp(2*x - b_val)
def H(x):
    # 원래 문제의 식: (f*g)' - 2f
    return fp(x)*g(x) + f(x)*gp(x) - 2*f(x)

# (가) 검증: k = b/2가 f(k)=g(k)=0이며 (-pi/2, pi/2)에 존재
k = b_val/2.0
cond_a = (abs(f(k)) < 1e-10 and abs(g(k)) < 1e-10 and -np.pi/2 < k < np.pi/2)

# (나) 검증: 원래 방정식의 모든 해를 (-pi/2, pi/2)에서 수치적으로 찾고 합이 pi/4인지
N = 300000
xs = np.linspace(-np.pi/2 + 1e-8, np.pi/2 - 1e-8, N)
Hs = H(xs)
raw_roots = []
for i in range(N-1):
    if Hs[i] == 0.0:
        raw_roots.append(xs[i])
    elif Hs[i]*Hs[i+1] < 0:
        lo, hi = xs[i], xs[i+1]
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if H(lo)*H(mid) <= 0:
                hi = mid
            else:
                lo = mid
        raw_roots.append(0.5*(lo+hi))

raw_roots.sort()
roots = []
for r in raw_roots:
    if not roots or r - roots[-1] > 1e-6:
        roots.append(r)

sum_roots = sum(roots)
cond_b = abs(sum_roots - np.pi/4) < 1e-6

if cond_a and cond_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
