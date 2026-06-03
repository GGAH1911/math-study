from fractions import Fraction
from itertools import product

# 카드별 (흰, 검) 증가량 — 문제 원문 그대로
delta = {1: (1, 0), 2: (1, 1), 3: (1, 1), 4: (2, 1)}

count_total_8 = 0
count_black_2 = 0
# 4번 복원추출, 각 카드 동등 확률 → 수열 4^4=256개를 전수조사
for seq in product([1, 2, 3, 4], repeat=4):
    w = sum(delta[c][0] for c in seq)
    b = sum(delta[c][1] for c in seq)
    if w + b == 8:
        count_total_8 += 1
        if b == 2:
            count_black_2 += 1

# 조건부 확률 P(검=2 | 총=8)
p = Fraction(count_black_2, count_total_8)
expected = Fraction(3, 35)
print('VERIFY_PASS' if p == expected else f'VERIFY_FAIL got={p}')