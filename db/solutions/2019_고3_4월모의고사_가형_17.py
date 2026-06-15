from itertools import product
from math import comb

def H(n, r):
    return comb(n + r - 1, r)

W, B, K = 6, 6, 3  # 흰6, 검6, 주머니3

def dists(total):
    res = []
    for a in range(total + 1):
        for b in range(total - a + 1):
            res.append((a, b, total - a - b))
    return res

whites = dists(W)
blacks = dists(B)

# 원식 그대로 완전탐색: 흰/검을 3주머니에 분배, 빈 주머니 없는 경우를 n으로 분류
case = {1: 0, 2: 0, 3: 0}
for w in whites:
    n = sum(1 for x in w if x > 0)
    if n == 0:
        continue
    for bk in blacks:
        if all(w[i] + bk[i] >= 1 for i in range(K)):
            case[n] += 1

H33 = H(3, 3)  # 흰 공을 세 주머니에 각 1개 이상 = 10
assert case[3] % H33 == 0
p = case[3] // H33      # (가)
q = case[2]            # (나)
r = case[1]            # (다)
total = p + q + r

# 교차검증: 빈 주머니 없는 전체 경우의 수 (포함배제)
ie = sum((-1) ** j * comb(K, j)
         * (comb((K - j) + W - 1, W) if K - j > 0 else 0)
         * (comb((K - j) + B - 1, B) if K - j > 0 else 0)
         for j in range(K + 1))
no_empty_brute = case[1] + case[2] + case[3]

print('p,q,r =', p, q, r, '| p+q+r =', total)
print('no-empty total brute=%d ie=%d' % (no_empty_brute, ie))

if (p == 28 and q == 315 and r == 45 and total == 388
        and no_empty_brute == ie == 640):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
