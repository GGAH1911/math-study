import numpy as np

sqrt2 = np.sqrt(2)

# Triangle from problem: AI=3, r=1, Area=5*sqrt(2)
a = 3*sqrt2       # BC
b = 5*sqrt2/2     # CA
c = 9*sqrt2/2     # AB
s = 5*sqrt2
hA = 10/3

B = np.array([0.0, 0.0])
C = np.array([a, 0.0])
A = np.array([23*sqrt2/6, hA])

assert abs(np.linalg.norm(A-B) - c) < 1e-9, 'AB fail'
assert abs(np.linalg.norm(A-C) - b) < 1e-9, 'AC fail'
assert abs(0.5*a*hA - 5*sqrt2) < 1e-9, 'Area fail'

I = (a*A + b*B + c*C)/(2*s)
assert abs(I[1] - 1.0) < 1e-9, 'r fail'
assert abs(np.linalg.norm(A-I) - 3.0) < 1e-9, 'AI fail'

k = (hA - 1)/hA  # = 7/10
D = A + k*(B - A)
E = A + k*(C - A)
assert abs(D[1]-1)<1e-9 and abs(E[1]-1)<1e-9

def angle_at(vtx, p1, p2):
    v1, v2 = p1-vtx, p2-vtx
    cos_a = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    return np.arccos(np.clip(cos_a,-1,1))

ang_BID = angle_at(I, B, D)
ang_IBD = angle_at(B, I, D)
gam_pass = abs(ang_BID - ang_IBD) < 1e-9

perim_ADE = np.linalg.norm(A-D)+np.linalg.norm(A-E)+np.linalg.norm(D-E)
nae_pass = abs(perim_ADE - 7*sqrt2) < 1e-9

DE = np.linalg.norm(D-E)
di_pass = abs(DE - 2*sqrt2) < 1e-9

if gam_pass and nae_pass and not di_pass:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'gam={gam_pass}, nae={nae_pass}, di={di_pass}')
    print(f'perim={perim_ADE:.8f}, 7sqrt2={7*sqrt2:.8f}')
    print(f'DE={DE:.8f}, 2sqrt2={2*sqrt2:.8f}')
