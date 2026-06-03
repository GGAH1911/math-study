import numpy as np
import math

# 원래 식의 큰 n에서의 합을 직접 계산
def partial_sum(n):
    k = np.arange(1, n+1, dtype=np.float64)
    return np.sum(k / (2.0*n - k)**2)

# 점점 큰 n으로 수렴 확인
vals = [partial_sum(n) for n in [1000, 10000, 100000, 1000000]]
limit_numeric = vals[-1]

# 후보 답 (보기 ②): 1 - ln 2
candidate = 1.0 - math.log(2.0)

# 다른 보기들도 비교
others = {
    '1': 1.5 - 2*math.log(2),
    '2': 1 - math.log(2),
    '3': 1.5 - math.log(3),
    '4': math.log(2),
    '5': 2 - math.log(3),
}

best = min(others.items(), key=lambda kv: abs(kv[1] - limit_numeric))

if best[0] == '2' and abs(limit_numeric - candidate) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
