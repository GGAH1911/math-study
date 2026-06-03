import numpy as np

a = -2/3
b = np.log(9/2) - 4/3

def h(x):
    return np.log(x**2 + x + 5/2) - a*x - b

def hprime(x):
    return (2*x + 1) / (x**2 + x + 5/2) - a

def hprimeprime(x):
    return -2*(x+2)*(x-1) / (x**2 + x + 5/2)**2

# f(x) > 0 iff h(x) > 0 (since g^{-1} is increasing, g^{-1}(0)=0)
cond1 = h(-3) * h(3) < 0  # f(-3)*f(3) < 0

# sign(f'(2)) = sign(h'(2)) since denominator 5f^4+3f^2 > 0
cond2 = hprime(2) > 0

# Differentiability: h vanishes to order 3 at x0=-2
cond3 = (abs(h(-2)) < 1e-12 and abs(hprime(-2)) < 1e-12 and abs(hprimeprime(-2)) < 1e-12)

# Answer value check
val = a * np.exp(b)
expected = -3 * np.exp(-4/3)
cond4 = abs(val - expected) < 1e-10

if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')