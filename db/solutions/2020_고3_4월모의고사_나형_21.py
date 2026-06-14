import math

def compute_f(t):
    total = 0
    for n in range(1, 1000):
        d_plus = n + 1
        d_minus = n - 1
        if math.isclose(d_plus, t, rel_tol=0, abs_tol=1e-9):
            total += 1
        elif d_plus < t:
            total += 2
        if math.isclose(d_minus, t, rel_tol=0, abs_tol=1e-9):
            total += 1
        elif d_minus < t:
            total += 2
        if d_minus > t + 1 and d_plus > t + 1:
            break
    return total

# Statement ㄱ: f(1/2) == 2
assert compute_f(0.5) == 2, f'FAIL ㄱ: {compute_f(0.5)}'

# Statement ㄴ: lim_{t->1+} f(t) != f(1)
f1 = compute_f(1.0)
f1r = compute_f(1.0 + 1e-8)
assert f1r != f1, f'FAIL ㄴ: lim={f1r}, f(1)={f1}'

# Statement ㄷ: exactly 3 discontinuities in (0, 4)
disc = 0
for a in [1.0, 2.0, 3.0]:
    fl = compute_f(a - 1e-8)
    fa = compute_f(a)
    fr = compute_f(a + 1e-8)
    if fl != fa or fr != fa:
        disc += 1
for t_val in [0.3, 0.7, 1.5, 2.5, 3.5]:
    fl = compute_f(t_val - 1e-8)
    fa = compute_f(t_val)
    fr = compute_f(t_val + 1e-8)
    assert fl == fa and fr == fa, f'Unexpected disc at t={t_val}'
assert disc == 3, f'FAIL ㄷ: {disc}'

print('VERIFY_PASS')
