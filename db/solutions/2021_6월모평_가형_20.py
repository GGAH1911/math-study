import numpy as np

# ---- original problem conditions ----
AB1, AC1, ang = 3.0, 2.0, np.pi/3
A  = np.array([0.0,0.0])
h  = ang/2
B1 = AB1*np.array([np.cos(h), np.sin(h)])
C1 = AC1*np.array([np.cos(-h), np.sin(-h)])
# angle bisector meets B1C1 at D1 with B1D1:D1C1 = AB1:AC1
t  = AB1/(AB1+AC1)
D1 = B1 + t*(C1-B1)

def circle(P,Q,R):
    ax,ay=P; bx,by=Q; cx,cy=R
    d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    ux=((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    uy=((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    c=np.array([ux,uy]); return c, np.linalg.norm(P-c)

O,r = circle(A,D1,C1)

# second intersection of circle with line A->B1 (s = signed distance from A)
u = (B1-A)/np.linalg.norm(B1-A)
b = 2*np.dot(u, A-O); c0 = np.dot(A-O,A-O)-r*r
roots=[(-b+np.sqrt(b*b-4*c0))/2, (-b-np.sqrt(b*b-4*c0))/2]
sB2 = min(s for s in roots if s>1e-9)
B2 = A + sB2*u
k  = sB2/AB1

def minor_arc(P,Q,n=4000):
    aP=np.arctan2(P[1]-O[1],P[0]-O[0]); aQ=np.arctan2(Q[1]-O[1],Q[0]-O[0])
    d=aQ-aP
    while d> np.pi: d-=2*np.pi
    while d<-np.pi: d+=2*np.pi
    ts=np.linspace(aP,aP+d,n)
    return np.array([O+r*np.array([np.cos(z),np.sin(z)]) for z in ts])

def shoelace(poly):
    x=poly[:,0]; y=poly[:,1]
    return 0.5*abs(np.dot(x,np.roll(y,-1))-np.dot(y,np.roll(x,-1)))

# Region1: B1 -> B2 -> arc(B2->D1) -> D1 (curvilinear triangle)
poly1 = np.vstack([B1, B2, minor_arc(B2,D1), D1])
area1 = shoelace(poly1)
# Region2: chord D1->C1 + arc(C1->D1) = circular segment
poly2 = np.vstack([D1, C1, minor_arc(C1,D1)])
area2 = shoelace(poly2)

A1    = area1 + area2
limit = A1/(1-k*k)
cand  = 27*np.sqrt(3)/46

# sanity: similarity ratio realized by next-step triangle (B2C2 || B1C1)
assert abs(k-8/15)<1e-9
print('limit=',limit,' candidate=',cand)
print('VERIFY_PASS' if abs(limit-cand)<1e-4 else 'VERIFY_FAIL')
