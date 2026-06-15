from math import perm, comb

# 2020 수능 나형 22: 7P2 + 7C2 의 값.
CANDIDATE = 63
print('VERIFY_PASS' if perm(7, 2) + comb(7, 2) == CANDIDATE else 'VERIFY_FAIL')
