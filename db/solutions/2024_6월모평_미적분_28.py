import numpy as np

a = 1/8
b = -7/8

def phi(u):
    return a * u**3 * np.exp(1 - u**2) + b + 1

def g(x):
    return a * np.cos(np.pi*x)**3 * np.exp(np.sin(np.pi*x)**2) + b

# phi >= 0 on [-1,1]
u_test = np.linspace(-1, 1, 100000)
phi_test = phi(u_test)
assert np.all(phi_test >= -1e-12)

# phi(-1)=0 (연속성 확보), phi(1)=1/4
assert abs(phi(-1)) < 1e-10
assert abs(phi(1) - 0.25) < 1e-10

# phi 단조증가
dphi = np.diff(phi_test)
assert np.all(dphi >= -1e-8)

# f(0)=-1/2 (+가지), f(2)=-3/2 (-가지)
f0 = +np.sqrt(phi(np.cos(0))) - 1
f2 = -np.sqrt(phi(np.cos(2*np.pi))) - 1
assert abs(f0 - (-0.5)) < 1e-10
assert abs(f2 - (-1.5)) < 1e-10

# 조건 (나): f(0) = f(2) + 1
assert abs(f0 - (f2 + 1)) < 1e-10

# 조건 (가) at x=0, x=2
assert abs(f0**2 + 2*f0 - g(0)) < 1e-10
assert abs(f2**2 + 2*f2 - g(2)) < 1e-10

# a*b = -7/64
assert abs(a * b - (-7/64)) < 1e-12

print('VERIFY_PASS')