import numpy as np

def distinct_real_root_count(k, tol=1e-7):
    coeffs = [1, -3, -9, k]
    roots = np.roots(coeffs)
    real_roots = []
    for r in roots:
        if abs(r.imag) < tol:
            real_roots.append(r.real)
    # cluster
    real_roots.sort()
    distinct = []
    for r in real_roots:
        if not distinct or abs(r - distinct[-1]) > 1e-5:
            distinct.append(r)
    return len(distinct)

# Find all k giving exactly 2 distinct real roots by scanning candidates
candidates = []
# Theoretically the cubic has exactly 2 distinct real roots iff discriminant = 0
# Discriminant of x^3+px+q after depression, but let's just check our two k values
for k in [-5, 27]:
    if distinct_real_root_count(k) == 2:
        candidates.append(k)

# Also scan a range to ensure no other k works
import numpy as _np
for k in _np.linspace(-100, 100, 20001):
    if distinct_real_root_count(k) == 2:
        # only count if not already in candidates (within tol)
        if not any(abs(k - c) < 1e-3 for c in candidates):
            candidates.append(float(k))

total = sum(candidates)
if abs(total - 22) < 1e-6 and set(candidates) == {-5, 27}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', candidates, total)
