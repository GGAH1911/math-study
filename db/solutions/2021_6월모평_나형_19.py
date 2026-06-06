import numpy as np

count_a = 0
valid_a = []

for a in range(-200, 201):
    coeffs = [2, 6, 0, a]
    roots = np.roots(coeffs)
    distinct_in_interval = []
    for r in roots:
        if abs(r.imag) < 1e-8:
            rv = r.real
            if -2 - 1e-8 <= rv <= 2 + 1e-8:
                is_new = all(abs(rv - e) > 1e-6 for e in distinct_in_interval)
                if is_new:
                    distinct_in_interval.append(rv)
    if len(distinct_in_interval) == 2:
        count_a += 1
        valid_a.append(a)

if count_a == 8 and valid_a == list(range(-8, 0)):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count_a}, valid_a={valid_a}')
