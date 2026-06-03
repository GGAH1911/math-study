import numpy as np

def S(t):
    xA = np.sqrt(np.log(1 + t))
    xB = np.sqrt(np.log(1 + 5*t))
    return (5*t / 2) * (xB - xA)

expected = (5/2) * (np.sqrt(5) - 1)
errors = []
for t in [1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
    ratio = S(t) / (t * np.sqrt(t))
    errors.append(abs(ratio - expected))

# 수렴 확인: 마지막 몇 개 오차가 충분히 작아야 함
if all(e < 1e-3 for e in errors[2:]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
