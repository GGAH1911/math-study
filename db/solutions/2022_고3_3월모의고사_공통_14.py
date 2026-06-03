import numpy as np

def distinct_real(coeffs, only_abs_ge_1=False, tol=1e-5):
    roots = np.roots(coeffs)
    real = [r.real for r in roots if abs(r.imag) < 1e-7]
    if only_abs_ge_1:
        real = [r for r in real if abs(r) >= 1 - 1e-7]
    real.sort()
    out = []
    for r in real:
        if not out or abs(r - out[-1]) > tol:
            out.append(r)
    return out

# ㄱ: k=0, f+g = x^3+2x^2+4 has 1 real root
ga = (len(distinct_real([1,2,0,4])) == 1)

# ㄴ: only k=4 gives 2 distinct real roots of x^3 - 2x^2 - kx + 8
at4 = (len(distinct_real([1,-2,-4,8])) == 2)
others = 0
for k in np.linspace(-30, 30, 30001):
    if abs(k - 4) < 0.005:
        continue
    if len(distinct_real([1,-2,-k,8])) == 2:
        others += 1
na = at4 and (others == 0)

# ㄷ: |f|=g has 5 distinct real roots for some k?
def count_abs(k):
    pr = distinct_real([1,-2,-k,8], only_abs_ge_1=True)
    qr = distinct_real([1, 2,-k,4], only_abs_ge_1=True)
    allr = sorted(pr + qr)
    out = []
    for r in allr:
        if not out or abs(r - out[-1]) > 1e-4:
            out.append(r)
    return len(out)

ks = list(np.linspace(-30, 30, 30001)) + list(np.linspace(6.5, 7.5, 5001)) + list(np.linspace(3.5, 4.5, 5001))
maxc = max(count_abs(k) for k in ks)
da = (maxc >= 5)

# Answer ② iff ㄱ True, ㄴ True, ㄷ False
if ga and na and (not da):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: g={ga}, n={na}, d={da}, maxc={maxc}')
