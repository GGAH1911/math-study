import math

def f(x):
    return math.cos(x) - 2 * math.pi / x

def bisect(lo, hi, tol=1e-13):
    flo = f(lo); fhi = f(hi)
    if flo * fhi >= 0:
        raise ValueError('no sign change')
    for _ in range(400):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if (hi - lo) < tol:
            return mid
        if flo * fmid < 0:
            hi = mid; fhi = fmid
        else:
            lo = mid; flo = fmid
    return (lo + hi) / 2

# Build a_m by finding positive roots of cos(x) - 2*pi/x in increasing order.
a = [2 * math.pi]  # a_1 (exact; cos(2pi)=1=2pi/(2pi))
a.append(bisect(2 * math.pi + 1e-7, 5 * math.pi / 2 - 1e-7))  # a_2
for k in range(2, 260):
    lo = 2 * math.pi * k - math.pi / 2 + 1e-9
    mid = 2 * math.pi * k
    hi = 2 * math.pi * k + math.pi / 2 - 1e-9
    # f(lo)<0, f(mid)>0, f(hi)<0
    a.append(bisect(lo, mid - 1e-9))
    a.append(bisect(mid + 1e-9, hi))

# Sanity: each a_m satisfies cos(a_m) == 2*pi/a_m (original equation)
for i, am in enumerate(a[:50]):
    assert abs(math.cos(am) - 2 * math.pi / am) < 1e-9, f'root failure at idx {i}'

def S(n):
    total = 0.0
    for k in range(1, n + 1):
        m = n + k
        total += n * math.cos(a[m - 1]) ** 2
    return total

s50 = S(50)
s100 = S(100)
print(f'S(50) = {s50}')
print(f'S(100) = {s100}')

if abs(s100 - 2) < 0.05 and abs(s50 - 2) < 0.1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
