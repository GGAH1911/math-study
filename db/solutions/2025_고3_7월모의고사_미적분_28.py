import math

def bisect(f, lo, hi, tol=1e-13, maxiter=400):
    flo, fhi = f(lo), f(hi)
    assert flo*fhi < 0
    for _ in range(maxiter):
        mid = (lo+hi)/2
        fmid = f(mid)
        if abs(fmid) < tol:
            return mid
        if flo*fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return (lo+hi)/2

# f(x) from the problem; f'(x) for x<0 derived analytically
# Verify derivative numerically against the formula
for xv in [-0.5, -1.0, -1.5, -2.0]:
    eps = 1e-6
    num = (math.log(-(xv+eps))/(xv+eps) - math.log(-(xv-eps))/(xv-eps))/(2*eps)
    ana = (1 - math.log(-xv))/xv**2
    assert abs(num-ana) < 1e-6

# g(1): solve (1 - ln(-x))/x^2 = 1, x in (-e, 0)
g1 = bisect(lambda x: (1 - math.log(-x))/x**2 - 1, -2.5, -0.5)
assert abs(g1 - (-1)) < 1e-10

# Count distinct intersections of y=f(x) and y=t*x+k for given a
def num_intersections(t, k, a):
    cnt = 0
    # Right (x>=0): x^2 - (2-t)x + (k-a) = 0
    B = -(2-t); C = k - a
    disc = B*B - 4*C
    if disc > 1e-13:
        sd = math.sqrt(disc)
        for s in (1, -1):
            x = (-B + s*sd)/2
            if x >= -1e-12: cnt += 1
    elif disc >= -1e-13:
        x = -B/2
        if x >= -1e-12: cnt += 1
    # Left (x<0): ln(-x)/x = tx+k => with u=-x>0: H(u)=ln(u)-t*u^2+k*u = 0
    # H has unique positive critical point (max) at root of 2tu^2 - ku - 1 = 0
    u_crit = (k + math.sqrt(k*k + 8*t))/(4*t)
    H_crit = math.log(u_crit) - t*u_crit**2 + k*u_crit
    if H_crit > 1e-10:
        cnt += 2
    elif H_crit >= -1e-10:
        cnt += 1
    return cnt

# h(t): a = m(t) - (2-t)^2/4 where m(t) = min K_t(u) = t*u - ln(u)/u
def m(t):
    us = bisect(lambda u: t*u*u - 1 + math.log(u), 1e-6, 100.0)
    return t*us - math.log(us)/us

def h(t):
    return m(t) - (2-t)**2/4

# Verify the original condition holds at t=1, a=h(1)
a1 = h(1)
assert abs(a1 - 0.75) < 1e-9
for k in [a1, a1+0.05, a1+0.15, a1+0.25, a1+0.5, a1+1.0, a1+2.0, a1+5.0]:
    n = num_intersections(1.0, k, a1)
    if n != 2:
        print('VERIFY_FAIL'); raise SystemExit
# And condition should fail for a slightly different from h(1)
for a_bad in [a1 - 0.05, a1 + 0.05]:
    fail_found = False
    for k in [a_bad, a_bad+0.05, a_bad+0.25, a_bad+0.5, a_bad+1.0]:
        if num_intersections(1.0, k, a_bad) != 2:
            fail_found = True; break
    if not fail_found:
        print('VERIFY_FAIL'); raise SystemExit

# h'(1) via central finite difference
eps = 1e-5
hp1 = (h(1+eps) - h(1-eps))/(2*eps)
assert abs(hp1 - 1.5) < 1e-5

result = g1 + hp1
if abs(result - 0.5) < 1e-5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
