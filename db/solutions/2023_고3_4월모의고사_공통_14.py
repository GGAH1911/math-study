def M_min_max(t):
    pts = [-2.0, 1.0]
    if -2 <= -t <= 1:
        pts.append(-t)
    if -2 <= t <= 1:
        pts.append(t)
    vals = [p**3 - 3*t*t*p for p in pts]
    return min(vals), max(vals)

def g(t):
    mn, mx = M_min_max(t)
    return mx + max(mx, -mn)

def two_f_neg_t(t):
    x = -t
    return 2 * (x**3 - 3*t*t*x)

# ㄱ: g(2) = 32
g2 = g(2.0)
g_true = abs(g2 - 32) < 1e-9

# ㄴ: solve g(t) = 2 f(-t) numerically over (0, 3]
ts = [i * 0.0005 for i in range(1, 6001)]
sol_ts = [t for t in ts if abs(g(t) - two_f_neg_t(t)) < 1e-7]
if sol_ts:
    sum_ext = min(sol_ts) + max(sol_ts)
    n_true = abs(sum_ext - 3.0) < 0.01
else:
    n_true = False

# ㄷ: difference of one-sided derivatives at t = 1/2
h = 1e-7
right = (g(0.5 + h) - g(0.5)) / h
left = (g(0.5 - h) - g(0.5)) / (-h)
diff_val = right - left
d_true = abs(diff_val - 5.0) < 0.01

chosen_answer = 3  # ㄱ, ㄴ
# Expected: ㄱ True, ㄴ True, ㄷ False  => answer 3
ok = g_true and n_true and (not d_true) and chosen_answer == 3
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
