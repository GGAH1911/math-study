import numpy as np

def verify(a):
    xs = np.linspace(0, np.pi, 100000)
    vals = np.sin(xs + a)
    M = vals.max()
    m = vals.min()
    return abs(2*abs(M) - abs(m)) < 1e-6

candidates = [5*np.pi/6, 7*np.pi/6, 17*np.pi/6]
results = [verify(a) for a in candidates]

# 확인: 세 값 모두 조건 만족, 합이 29π/6인지
total = sum(candidates)
expected = 29*np.pi/6

if all(results) and abs(total - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
