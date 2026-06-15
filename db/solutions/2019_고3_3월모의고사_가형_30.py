CANDIDATE = 77
from collections import Counter

def works(roots, k):
    # |f(g(x))| differentiable iff every SIMPLE root r satisfies r >= 3+k
    for r, m in roots.items():
        if m == 1 and r < 3 + k:
            return False
    return True

def f0(roots):
    v = 1
    for r, m in roots.items():
        v *= (0 - r) ** m
    return v

valid = []
seen = set()
for a in range(1, 11):
    for b in range(a, 11):
        roots = Counter([1, 1, a, b])  # (x-1)^2 (x-a)(x-b), leading coeff 1
        key = tuple(sorted(roots.items()))
        if key in seen:
            continue
        seen.add(key)
        # condition (da): exactly 4 natural k make |f o g| differentiable
        cnt = sum(1 for k in range(1, 500) if works(roots, k))
        # must have at least one simple root (else infinite k)
        has_simple = any(m == 1 for m in roots.values())
        if cnt == 4 and has_simple:
            valid.append(f0(roots))

if not valid:
    print('VERIFY_FAIL')
else:
    result = max(valid) + min(valid)
    print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')
