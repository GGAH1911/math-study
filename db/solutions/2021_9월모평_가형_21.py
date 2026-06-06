import numpy as np
def h(k,x): return np.sin(k*x)+2-3*np.cos(12*x)
def roots(k,N=400000):
    xs=np.linspace(-2*np.pi,2*np.pi,N); hv=h(k,xs); r=[]
    s=np.sign(hv); idx=np.where(s[:-1]*s[1:]<0)[0]
    for i in idx:
        a,b=xs[i],xs[i+1]; fa=h(k,a)
        for _ in range(100):
            m=0.5*(a+b); fm=h(k,m)
            if fa*fm<=0: b=m
            else: a=m; fa=fm
        r.append(0.5*(a+b))
    ah=np.abs(hv)
    for i in range(1,N-1):
        if ah[i]<ah[i-1] and ah[i]<ah[i+1] and ah[i]<1e-2:
            a,b=xs[i-1],xs[i+1]
            for _ in range(150):
                m1=a+(b-a)/3; m2=b-(b-a)/3
                if abs(h(k,m1))<abs(h(k,m2)): b=m2
                else: a=m1
            xm=0.5*(a+b)
            if abs(h(k,xm))<1e-7: r.append(xm)
    return r
def ok(k):
    av=sorted(np.sin(k*x)+2 for x in roots(k)); g=[]
    for a in av:
        if not g or abs(a-g[-1])>1e-5: g.append(a)
    L,R=-2*np.pi,2*np.pi
    for a in g:
        s=min(1.0,max(-1.0,a-2.0)); asin=np.arcsin(s); nm=int(k*4)+5
        for n in range(-nm,nm+1):
            for base in (asin,np.pi-asin):
                q=(base+2*np.pi*n)/k
                if L-1e-9<=q<=R+1e-9 and abs(3*np.cos(12*q)-a)>1e-4: return False
    return True
good=[k for k in range(1,51) if ok(k)]
print('VERIFY_PASS' if good==[1,2,3,6] and len(good)==4 else 'VERIFY_FAIL')