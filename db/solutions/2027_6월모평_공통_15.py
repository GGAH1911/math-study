import numpy as np

def f(x):
    x = np.asarray(x, dtype=float)
    return 0.25 * x**2 * (x - 3.0)

# f(6) = 27
assert abs(float(f(6)) - 27.0) < 1e-9, f'f(6) = {float(f(6))}'

# constant term 0 and cubic: verified by construction (f(0)=0, leading x^3 coef = 1/4)
assert abs(float(f(0))) < 1e-12

def trap(g, a, b, n=40001):
    xs = np.linspace(a, b, n)
    ys = g(xs)
    h = (b - a) / (n - 1)
    return h * (np.sum(ys) - 0.5 * (ys[0] + ys[-1]))

# Condition (가): differ iff 0 < p < 3
for p in [0.05, 0.5, 1.0, 1.5, 2.0, 2.5, 2.95]:
    A = trap(lambda x: np.abs(f(x)), p, p + 3)
    B = trap(lambda x: f(x), p, p + 3)
    assert A - abs(B) > 1e-3, f'(가) should differ at p={p}, got diff={A-abs(B)}'

for p in [-2.0, -1.0, -0.5, -0.05, 0.0, 3.0, 3.05, 3.5, 5.0]:
    A = trap(lambda x: np.abs(f(x)), p, p + 3)
    B = trap(lambda x: f(x), p, p + 3)
    assert abs(A - abs(B)) < 1e-3, f'(가) should be equal at p={p}, got diff={A-abs(B)}'

# Condition (나): differ iff 0 < q < 1
for q in [0.05, 0.25, 0.5, 0.75, 0.95]:
    A = trap(lambda x: np.abs(f(x) + q), 0.0, 3.0)
    B = trap(lambda x: f(x) + q, 0.0, 3.0)
    assert A - abs(B) > 1e-3, f'(나) should differ at q={q}'

for q in [-1.0, -0.5, -0.05, 0.0, 1.0, 1.05, 1.5, 2.0]:
    A = trap(lambda x: np.abs(f(x) + q), 0.0, 3.0)
    B = trap(lambda x: f(x) + q, 0.0, 3.0)
    assert abs(A - abs(B)) < 1e-3, f'(나) should be equal at q={q}, got diff={A-abs(B)}'

print('VERIFY_PASS')
