import numpy as np

def f(t):
    return t**3 - 3*t**2 + 3*t

def fprime(t):
    return 3*t**2 - 6*t + 3

def g(val):
    diff = val - 1
    if diff >= 0:
        return diff**(1/3) + 1
    else:
        return -((-diff)**(1/3)) + 1

alpha = 2

# f(0)=0
assert abs(f(0)) < 1e-10, 'FAIL: f(0)!=0'

# f(alpha)=alpha (fixed point)
assert abs(f(alpha) - alpha) < 1e-10, 'FAIL: f(alpha)!=alpha'

# f'(alpha)=3
assert abs(fprime(alpha) - 3) < 1e-10, 'FAIL: f_prime(alpha)!=3'

# h(0)=1
g0 = g(0)
h0 = (g0 - alpha) / (0 - alpha)
assert abs(h0 - 1) < 1e-10, f'FAIL: h(0)={h0}!=1'

# g'(alpha)=1/3 (continuity at x=alpha)
gprime_alpha = 1 / fprime(g(alpha))
assert abs(gprime_alpha - 1/3) < 1e-10, f'FAIL: g_prime(alpha)={gprime_alpha}!=1/3'

# f'(x)>=0 all x (monotone): check discriminant
a_val = -3.0
b_val = 3.0
disc = (2*a_val)**2 - 4*3*b_val
assert disc <= 1e-10, f'FAIL: f_prime not nonneg, disc={disc}'

# Compute alpha*h(9)*g'(9)
g9 = g(9)
h9 = (g9 - alpha) / (9 - alpha)
gprime9 = 1.0 / fprime(g9)
result = alpha * h9 * gprime9

expected = 1.0 / 42.0
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: result={result}, expected={expected}')
