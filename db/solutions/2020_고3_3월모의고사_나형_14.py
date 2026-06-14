from itertools import product
from collections import Counter

digits = [1, 2, 3]
even_positions = {2, 4, 6}  # 1-indexed even slots

def valid(s):
    # each of 1,2,3 used at least once
    if not (1 in s and 2 in s and 3 in s):
        return False
    # every '2' must sit at an even position (positions are 1-indexed)
    for i in range(1, 8):
        if s[i - 1] == 2 and i not in even_positions:
            return False
    return True

all_valid = [s for s in product(digits, repeat=7) if valid(s)]
total = len(all_valid)
cnt2 = Counter(s.count(2) for s in all_valid)

# (gae) p: one '2' fixed at a single even slot, remaining 6 slots filled by {1,3}, each at least once
p = sum(1 for t in product([1, 3], repeat=6) if (1 in t and 3 in t))
# (na) q: total when exactly one '2' is used
q = cnt2[1]
# (da) r: total when exactly three '2's are used
r = cnt2[3]

answer_value = p + q + r

ok = (total == 290) and (p == 62) and (q == 186) and (r == 14) and (answer_value == 262)
print('p,q,r =', p, q, r, '| sum =', answer_value, '| total =', total)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
