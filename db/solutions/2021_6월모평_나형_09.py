import numpy as np

# f(x) = 2^|x| on [-1, 3]
xs = np.linspace(-1, 3, 100000)
fxs = 2 ** np.abs(xs)

max_val = fxs.max()
min_val = fxs.min()
total = max_val + min_val

# Exact values
import sympy as sp
x = sp.Symbol('x')
f = 2**sp.Abs(x)
candidates = [f.subs(x, v) for v in [-1, 0, 1, 2, 3]]
exact_max = max(candidates)
exact_min = min(candidates)
exact_sum = exact_max + exact_min

CANDIDATE = 9
if exact_sum == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {exact_sum}')
