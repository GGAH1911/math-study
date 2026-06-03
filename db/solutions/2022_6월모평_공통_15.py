import math

def find_root(f, a, b, n=100):
    fa, fb = f(a), f(b)
    if fa == 0: return a
    if fb == 0: return b
    if fa * fb > 0: return None
    for _ in range(n):
        m = (a + b) / 2
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2

def roots_in_0_4(t):
    roots = []
    for f in [lambda x: math.sin(math.pi * x / 2) - t,
              lambda x: math.cos(math.pi * x / 2) - t]:
        N = 4000
        h = 4.0 / N
        prev_x = 0.0
        prev_v = f(prev_x)
        for i in range(1, N + 1):
            x = i * h
            v = f(x)
            if prev_v == 0 and prev_x < 4:
                roots.append(prev_x)
            elif prev_v * v < 0:
                r = find_root(f, prev_x, x)
                if r is not None and 0 <= r < 4:
                    roots.append(r)
            prev_x, prev_v = x, v
    return sorted(set(round(r, 8) for r in roots))

def alpha_beta(t):
    rs = roots_in_0_4(t)
    return rs[0], rs[-1]

# ㄱ: alpha+beta = 5 for t in [-1, 0)
ok_g = True
for t in [-1.0, -0.9, -0.7, -0.5, -0.3, -0.1, -0.01]:
    a, b = alpha_beta(t)
    if abs(a + b - 5) > 1e-4:
        ok_g = False
        break

# ㄴ: beta - alpha = 3 iff t in [0, sqrt(2)/2]
ok_n_inside = True
for t in [0.0, 0.1, 0.3, 0.5, math.sqrt(2)/2 - 1e-6, math.sqrt(2)/2]:
    a, b = alpha_beta(t)
    if abs(b - a - 3) > 1e-4:
        ok_n_inside = False
        break
ok_n_outside = True
for t in [-0.7, -0.3, 0.8, 0.9, 0.99]:
    a, b = alpha_beta(t)
    if abs(b - a - 3) < 1e-4:
        ok_n_outside = False
        break
ok_n = ok_n_inside and ok_n_outside

# ㄷ: pair with alpha(t1)=alpha(t2), t2-t1=0.5 gives t1*t2=3/8 (NOT 1/3, so ㄷ false)
t1 = (math.sqrt(7) - 1) / 4
t2 = t1 + 0.5
a1, _ = alpha_beta(t1)
a2, _ = alpha_beta(t2)
premise_ok = abs(a1 - a2) < 1e-4
prod = t1 * t2
ok_d_false = premise_ok and abs(prod - 1/3) > 1e-3 and abs(prod - 3/8) < 1e-6

if ok_g and ok_n and ok_d_false:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL g={ok_g} n={ok_n} d_false={ok_d_false} prod={prod}')
