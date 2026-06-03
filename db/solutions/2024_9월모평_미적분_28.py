import math

def fval(t, a):
    if t < 0:
        return 2.0*abs(math.sin(4.0*t))
    return -math.sin(a*t)

def F(x, a, N=4000):
    lo = -a*math.pi
    if abs(x - lo) < 1e-15:
        return 0.0
    if x < lo:
        a_, b_, sign = x, lo, -1.0
    else:
        a_, b_, sign = lo, x, 1.0
    h = (b_ - a_)/N
    s = 0.5*(fval(a_, a) + fval(b_, a))
    for j in range(1, N):
        s += fval(a_ + j*h, a)
    return sign*s*h

def main():
    a = 3.0/4.0
    # (1) f(-a*pi) must vanish so that g=|F| is differentiable at the forced zero x=-a*pi
    if abs(fval(-a*math.pi, a)) > 1e-8:
        print('VERIFY_FAIL'); return
    # (2) For x>=0, F(x) must stay strictly positive (no other zeros)
    for i in range(1, 401):
        x = i*(4.0*math.pi/400.0)
        if F(x, a, N=2000) <= 1e-3:
            print('VERIFY_FAIL'); return
    # (3) Smaller candidate a=1/2: F(pi)=0 but f(pi)!=0  -> g not differentiable
    Fp = F(math.pi, 0.5, N=6000)
    if abs(Fp) > 0.02 or abs(fval(math.pi, 0.5)) < 0.5:
        print('VERIFY_FAIL'); return
    # (4) Smaller candidate a=1/4: at x=4*arccos(3/4), F=0 but f!=0
    x0 = 4.0*math.acos(0.75)
    Fz = F(x0, 0.25, N=6000)
    if abs(Fz) > 0.02 or abs(fval(x0, 0.25)) < 0.3:
        print('VERIFY_FAIL'); return
    # (5) Any a not of the form k/4 violates step (1); among k/4 in (0,2) the smallest passing is 3/4
    print('VERIFY_PASS')

main()
