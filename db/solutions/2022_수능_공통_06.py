import numpy as np

def count_distinct_real_roots(k):
    coeffs = [2, -3, -12, k]
    roots = np.roots(coeffs)
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
    unique_real = []
    for r in real_roots:
        if all(abs(r - u) > 1e-6 for u in unique_real):
            unique_real.append(r)
    return len(unique_real)

count = sum(1 for k in range(-6, 20) if count_distinct_real_roots(k) == 3)

# Boundary check: k=-7 and k=20 should NOT give 3 distinct roots
boundary_ok = (count_distinct_real_roots(-7) != 3 and count_distinct_real_roots(20) != 3)

if count == 26 and boundary_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}, boundary_ok={boundary_ok}')
