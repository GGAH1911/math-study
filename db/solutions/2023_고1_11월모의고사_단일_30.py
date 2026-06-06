import numpy as np
t_values = [1, 6, 10, 15, 20]
m = 6
for t in t_values:
    f_roots = [-1 - np.sqrt(1+t), -1 + np.sqrt(1+t)] if 1+t >= 0 else []
    g_roots = [m - np.sqrt(t-m), m + np.sqrt(t-m)] if t >= m else []
    all_roots = sorted(set(np.round([*f_roots, *g_roots], 10)))
    h_t = sum(all_roots)
    f_check = all(abs(x**2 + 2*x - t) < 1e-9 for x in f_roots)
    g_check = all(abs((x-m)**2 + m - t) < 1e-9 for x in g_roots)
    assert f_check and g_check, f't={t} failed'
print('VERIFY_PASS')