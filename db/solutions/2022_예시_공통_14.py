import numpy as np
from numpy.polynomial import polynomial as P

results = []

# v(t) = t^3 - 6t^2 + 9t + k, derived from a(t)=3t^2-12t+9 with v(0)=k

# ㄱ: on (3, inf), velocity increasing  <=> a(t) > 0
# a(t) = 3t^2 - 12t + 9 = 3(t-1)(t-3); for t>3, a>0
ts = np.linspace(3.001, 20, 2000)
a_vals = 3*ts**2 - 12*ts + 9
g1 = np.all(a_vals > 0)
results.append(('ㄱ', g1, True))

# ㄴ: k=-4, direction changes twice on (0, inf)?
k = -4
ts = np.linspace(1e-6, 20, 200000)
v = ts**3 - 6*ts**2 + 9*ts + k
signs = np.sign(v)
# count sign changes (ignoring zeros)
nz = signs[signs != 0]
changes = int(np.sum(np.diff(nz) != 0))
g2 = (changes == 2)
results.append(('ㄴ', g2, False))

# ㄷ: minimum k such that pos change = distance on [0,5]
# Equivalent to min k such that v(t) >= 0 on [0,5]
# = -min_{t in [0,5]} f(t), where f(t)=t^3-6t^2+9t
# f'(t)=3(t-1)(t-3): crit pts t=1,3. f(0)=0, f(1)=4, f(3)=0, f(5)=20. min=0.
# So min k = 0. Verify: at k=0, v(t)=t(t-3)^2 >= 0 on [0,5].
ts = np.linspace(0, 5, 100000)
v0 = ts**3 - 6*ts**2 + 9*ts + 0
g3a = np.all(v0 >= -1e-12)
# And for k slightly less than 0, must fail
v_neg = ts**3 - 6*ts**2 + 9*ts + (-0.01)
g3b = np.any(v_neg < 0)
g3 = g3a and g3b
results.append(('ㄷ', g3, True))

# Final answer is ㄱ, ㄷ = option 4
truth = {name: actual == expected for name, actual, expected in results}
print('checks:', truth)
if truth['ㄱ'] and truth['ㄴ'] and truth['ㄷ']:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
