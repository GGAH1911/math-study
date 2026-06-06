import math
from math import log

def f(x):
    return 0.0 if x<=0 else (log(1+x**4))**10

def h(t):
    return f(t)*f(1-t)

def integ(a,b,n=200000):
    s=0.0; dx=(b-a)/n
    for i in range(n):
        t=a+(i+0.5)*dx
        s+=h(t)*dx
    return s

# the=g over [0,1]; g for x<=0 is 0 since f(t)=0 there
# ㄱ: g(-3)=0
g_neg=integ(0,-3,200000)
# ㄴ: g(1)=2 g(1/2)
g1=integ(0,1)
ghalf=integ(0,0.5)
# ㄷ: max g = g(1) < 1
okA = abs(g_neg)<1e-30
okB = abs(g1-2*ghalf)<1e-30 or abs(g1-2*ghalf)<1e-12*max(1,abs(g1))
okC = g1<1
print('VERIFY_PASS' if (okA and okB and okC) else 'VERIFY_FAIL')
