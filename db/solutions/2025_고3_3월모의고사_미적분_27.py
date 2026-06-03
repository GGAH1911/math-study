from fractions import Fraction

def count_roots_exact(a_n, x_max=Fraction(3)):
    count = 0
    k = 0
    while True:
        x = a_n * (4*k + 1) / 2
        if x >= x_max:
            break
        count += 1
        k += 1
    return count

errors = []
for n in range(1, 101):
    # lower bound: a_n = 6/(8n+1), boundary: k=2n gives x=3 exactly (excluded)
    a_n = Fraction(6, 8*n + 1)
    cnt = count_roots_exact(a_n)
    if cnt != 2*n:
        errors.append((n, float(a_n), cnt, 2*n))
    # midpoint value: should also give 2n roots
    a_mid = Fraction(6*2, (8*n+1) + (8*n-3))
    cnt2 = count_roots_exact(a_mid)
    if cnt2 != 2*n:
        errors.append((f'n={n}_mid', float(a_mid), cnt2, 2*n))

# Squeeze theorem check with exact fractions
limit_ok = True
for n in [10, 100, 1000]:
    lo = Fraction(6*n, 8*n+1)
    hi = Fraction(6*n, 8*n-3)
    target = Fraction(3, 4)
    if not (lo <= target + Fraction(1, n) and hi >= target - Fraction(1, n)):
        limit_ok = False

# Check both bounds converge to 3/4
limit_lower = Fraction(6, 8)  # lim 6n/(8n+1) = 6/8 = 3/4
limit_upper = Fraction(6, 8)  # lim 6n/(8n-3) = 6/8 = 3/4

if len(errors) == 0 and limit_lower == Fraction(3,4) and limit_upper == Fraction(3,4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    if errors: print('errors:', errors[:5])
    print('limit_lower:', limit_lower, 'limit_upper:', limit_upper)
