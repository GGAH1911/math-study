from itertools import permutations
from math import gcd

# 1부터 13까지 순서쌍 중 gcd != 1인 경우
non_coprime = 0
for m, n in permutations(range(1, 14), 2):
    if gcd(m, n) != 1:
        non_coprime += 1

total_pairs = 13 * 12
result = total_pairs - non_coprime

p = 156
q = 6
r = non_coprime
ans = p + q + r

if ans == 204:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')