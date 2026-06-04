import numpy as np

a = 2.0
b = 5

# Original equation: (cos(b*pi*x) - 1/2) * (a*cos(b*pi*x) + (a+2)/2) = 0 on [0,2]
f = lambda x: (np.cos(b*np.pi*x) - 0.5) * (a*np.cos(b*np.pi*x) + (a+2)/2)

# Find roots by dense sampling and sign change + refinement via bisection
xs = np.linspace(0, 2, 200001)
ys = f(xs)

roots = []
for i in range(len(xs)-1):
    if ys[i] == 0:
        roots.append(xs[i])
    elif ys[i]*ys[i+1] < 0:
        # bisect
        lo, hi = xs[i], xs[i+1]
        for _ in range(80):
            m = (lo+hi)/2
            if f(lo)*f(m) <= 0:
                hi = m
            else:
                lo = m
        roots.append((lo+hi)/2)
# Also check endpoint x=2
if abs(ys[-1]) < 1e-9:
    roots.append(xs[-1])

# Deduplicate close roots
roots = sorted(roots)
uniq = []
for r in roots:
    if not uniq or abs(r-uniq[-1]) > 1e-5:
        uniq.append(r)

# Verify each root satisfies the original equation
all_ok = all(abs(f(r)) < 1e-6 for r in uniq)

if len(uniq) == 15 and all_ok and (a+b) == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', len(uniq), all_ok)
