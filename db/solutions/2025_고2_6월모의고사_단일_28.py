import numpy as np

k = 10

# n의 범위 계산
lower_bound = k - np.log2(k + 2)
upper_bound = k + 2 - np.log2(k)

n_min = int(np.ceil(lower_bound))
n_max = int(np.floor(upper_bound))

# f(k) 계산
f_k = n_max + n_min

# 검증: 실제로 각 n이 조건을 만족하는지 확인
verified = True
for n in [n_min - 1, n_min, n_max, n_max + 1]:
    t = 2 ** (-(n - k))
    cond1 = t <= k + 2
    cond2 = t >= k / 4
    if n == n_min:
        verified = verified and (cond1 and cond2)
    elif n == n_max:
        verified = verified and (cond1 and cond2)
    elif n == n_min - 1:
        verified = verified and (not (cond1 and cond2))
    elif n == n_max + 1:
        verified = verified and (not (cond1 and cond2))

if verified and f_k == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')