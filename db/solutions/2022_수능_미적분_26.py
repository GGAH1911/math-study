import numpy as np

# 원래 식의 부분합을 큰 n으로 수치 계산하여 ln5/3 에 수렴하는지 확인
def partial_sum(n):
    k = np.arange(1, n+1, dtype=float)
    return np.sum((k**2 + 2*k*n) / (k**3 + 3*k**2*n + n**3))

target = np.log(5) / 3

results = [partial_sum(n) for n in [10000, 100000, 1000000]]
errors = [abs(r - target) for r in results]

# 수렴 확인: 오차가 1e-4 미만이면 PASS
if all(e < 1e-4 for e in errors):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'results={results}, target={target}, errors={errors}')
