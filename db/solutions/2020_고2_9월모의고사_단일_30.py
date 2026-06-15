# f(x)=x²+2x+2. g(x)=f(x)(x<0), |f(-x)-t|(x>=0). h(t)=#{x:g(x)=t/3}.
# h 불연속 α 들에 대해 Σ 4 α h(α) ?
CANDIDATE = 141
def h(t):
    c = t/3.0; n = 0
    if c > 1+1e-9:                       # 좌측 x<0: (x+1)²=c-1
        r = (c-1)**0.5
        if -1-r < -1e-9: n += 1
        if -1+r < -1e-9: n += 1
    elif c > 1-1e-9:
        n += 1
    for R in (t-1+c, t-1-c):             # 우측 x>=0: (x-1)²=R, R=t-1±c
        if R < -1e-9: continue
        if R < 1e-9: n += 1
        else:
            r = R**0.5
            if 1+r >= 0: n += 1
            if 1-r >= -1e-9: n += 1
    return n
# 불연속 후보(경계): c=1→t=3, c=2→t=6, R1=0→3/4, R1=1→3/2, R2=0→3/2, R2=1→3
cands = sorted({3.0, 6.0, 3/4, 3/2})
eps = 1e-4
alphas = [a for a in cands if h(a-eps) != h(a+eps)]
total = sum(4*a*h(a) for a in alphas)
print('VERIFY_PASS' if abs(total - CANDIDATE) < 1e-6 else 'VERIFY_FAIL')
