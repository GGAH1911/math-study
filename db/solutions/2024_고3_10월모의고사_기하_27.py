import numpy as np
E=np.array([0,0,0.]); F=np.array([2,0,0.]); G=np.array([2,2,0.]); H=np.array([0,2,0.])
A=np.array([0,0,2.]); B=np.array([2,0,2.]); C=np.array([2,2,2.]); D=np.array([0,2,2.])
M=(D+H)/2; N=(G+H)/2
# minimize |NP| for P on segment FM
best=(1e18,None,None)
for t in np.linspace(0,1,200001):
    P=F+t*(M-F)
    d=np.linalg.norm(P-N)
    if d<best[0]: best=(d,t,P)
d_min,t_star,P_star=best
# projection of vector NP onto plane FHM
FH=H-F; FM=M-F
n=np.cross(FH,FM); n_unit=n/np.linalg.norm(n)
NP=P_star-N
comp_n=np.dot(NP,n_unit)
proj_plane=NP-comp_n*n_unit
len_proj=np.linalg.norm(proj_plane)
expected=np.sqrt(2)/2
if abs(len_proj-expected)<1e-4 and abs(d_min-1.0)<1e-4 and abs(t_star-2/3)<1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', d_min, t_star, len_proj, expected)