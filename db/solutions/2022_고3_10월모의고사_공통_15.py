def is_S_injective(p, N=300):
    vals = set()
    for n in range(1, N+1):
        s = p*n*n - 36*n  # q irrelevant for injectivity
        if s in vals:
            return False
        vals.add(s)
    return True

p1 = None
for p in range(1, 100):
    if is_S_injective(p):
        p1 = p
        break
assert p1 == 5, f'p1={p1}'

p = p1
valid_qs = []
for q in range(1, 2000):
    def S(n, q=q):
        return p*n*n - 36*n + q
    a1 = S(1)
    if a1 <= 0:
        continue
    count = 0
    for k in range(2, 500):
        ak = S(k) - S(k-1)
        if abs(ak) < a1:
            count += 1
    # also check k=1 for completeness
    if abs(a1) < a1:
        count += 1
    if count == 3:
        valid_qs.append(q)

total = sum(valid_qs)
print('VERIFY_PASS' if total == 372 else f'VERIFY_FAIL total={total} qs={valid_qs}')
