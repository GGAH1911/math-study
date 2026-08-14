# 상자 4개에 검은 4, 흰 6 을 남김없이 분배(같은 색끼리 구별 X).
# (가) 검은 공 없는 상자 ≥ 2  (나) 검은 공 있는 상자의 흰 공 ≤ 1
# 조건이 단순 열거로 끝나므로 모든 분배를 실제로 세어 보기와 대조한다.
import sympy as sp
from itertools import product

def comps(total, parts):
    """음이 아닌 정수 해 (x1..xk), 합 = total."""
    if parts == 1:
        yield (total,); return
    for first in range(total + 1):
        for rest in comps(total - first, parts - 1):
            yield (first,) + rest

cnt = 0
blacks = list(comps(4, 4))
whites = list(comps(6, 4))
for b in blacks:
    if sum(1 for x in b if x == 0) < 2:           # (가)
        continue
    for w in whites:
        if all(w[i] <= 1 for i in range(4) if b[i] >= 1):   # (나)
            cnt += 1
val = sp.Integer(cnt)
choices = {1: 580, 2: 592, 3: 604, 4: 616, 5: 628}
pick = [k for k, v in choices.items() if val == v]
print('VERIFY_PASS' if pick == [5] else 'VERIFY_FAIL')
