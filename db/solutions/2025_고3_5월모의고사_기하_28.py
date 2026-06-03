import numpy as np
sqrt2=np.sqrt(2);sqrt5=np.sqrt(5);sqrt6=np.sqrt(6)
t=1/sqrt2
A=np.array([0.0,t]);B=np.array([0.0,-t]);F=np.array([1.0,0.0])
P0=np.array([3/2,5*sqrt2/4])
ell=P0[0]**2/6+P0[1]**2/5
assert abs(ell-1)<1e-9,'P0 not on ellipse'
assert P0[0]>0 and P0[1]>0,'not first quadrant'
assert A[1]>0,'A y negative'
assert abs(A[1]-B[1])<2*sqrt5,'|AB| too large'
BF=np.linalg.norm(B-F);FP0=np.linalg.norm(F-P0);P0A=np.linalg.norm(P0-A)
total=BF+FP0+P0A
assert abs(total-2*sqrt6)<1e-8,f'sum={total} expected {2*sqrt6}'
area0=0.5*(P0[1]+t*(1+P0[0]))
for theta in np.linspace(0.001,np.pi/2-0.001,100000):
    Pt=np.array([sqrt6*np.cos(theta),sqrt5*np.sin(theta)])
    assert area0>=0.5*(Pt[1]+t*(1+Pt[0]))-1e-9,'P0 not max'
axb=P0[0]*P0[1];expected=15*sqrt2/8
if abs(axb-expected)<1e-9:print('VERIFY_PASS')
else:print(f'VERIFY_FAIL: {axb} vs {expected}')