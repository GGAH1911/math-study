import numpy as np
from math import pi, sin, cos

def gp(s):
    # sign of g'(x) as function of s=sqrt(x)
    return -pi*s*cos(pi*s)+sin(pi*s)

S=np.linspace(1e-9,13,3000000)
v=np.array([gp(x) for x in S])
maxes=[]
for i in range(len(S)-1):
    if v[i]*v[i+1]<0:
        a,b=S[i],S[i+1]
        for _ in range(80):
            m=(a+b)/2
            if gp(a)*gp(m)<=0: b=m
            else: a=m
        r=(a+b)/2
        if gp(r-1e-6)>0 and gp(r+1e-6)<0:
            maxes.append(r*r)
maxes.sort()
a6=maxes[5]
k=11
ok = (k**2 < a6 < (k+1)**2) and abs(a6-132.047)<0.5
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
