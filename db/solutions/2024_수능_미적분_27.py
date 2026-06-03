import math

def find_s(t):
    # Solve -(s+1)*exp(-s) = exp(t) for s < -1.
    # g(s) = -(s+1)*exp(-s) is decreasing on (-inf, -1) from +inf down to 0.
    target = math.exp(t)
    lo, hi = -100.0, -1.0 - 1e-14
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        val = -(mid + 1.0) * math.exp(-mid)
        if val > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def f(t):
    s = find_s(t)
    # Verify tangent condition with original curve y = e^{-x} + e^t:
    #   tangent slope at x=s is -e^{-s}; line through origin gives y = -e^{-s} x;
    #   curve value at x=s equals line value at x=s iff e^t = -(s+1)e^{-s}.
    assert s < -1.0
    # f(t) is the slope of that tangent line
    return -math.exp(-s)

# a is the constant satisfying f(a) = -e*sqrt(e) = -e^{3/2}.
# From e^{-s}=e^{3/2}, s=-3/2; then e^a = -(s+1)e^{-s} = (1/2) e^{3/2}.
a = 1.5 - math.log(2.0)

# Sanity-check f(a):
fa = f(a)
assert abs(fa - (-math.exp(1.5))) < 1e-8, fa

# Numerical derivative f'(a) from the ORIGINAL definition of f.
h = 1e-5
fpa_num = (f(a + h) - f(a - h)) / (2.0 * h)

candidate = -math.exp(1.5) / 3.0  # our answer: -e*sqrt(e)/3

if abs(fpa_num - candidate) < 1e-4:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
