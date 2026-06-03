import math

log3_2 = math.log(2)/math.log(3)
k = 17/4 + 2*log3_2
assert 5 < k < 6

def bisect(g,a,b,tol=1e-13,it=400):
    fa=g(a); fb=g(b)
    assert fa*fb<0
    for _ in range(it):
        c=(a+b)/2; fc=g(c)
        if abs(fc)<tol or (b-a)<tol: return c
        if fa*fc<0: b,fb=c,fc
        else: a,fa=c,fc
    return (a+b)/2

# Curve1: y = -log_3 x + 4. Intersection with line y=-x+k: log_3 x = x+4-k
f = lambda x: math.log(x,3) - x - 4 + k
a1 = bisect(f, 1e-4, 0.9)
a2 = bisect(f, 0.95, 5)
A = (a1, -math.log(a1,3)+4)
B = (a2, -math.log(a2,3)+4)

# Curve2: y = 3^{-x+4}. Intersection with line: 3^{-x+4} + x - k = 0
g = lambda x: 3**(-x+4) + x - k
cx = bisect(g, 2.5, 4.5)
dx = bisect(g, 4.5, 7)
C = (cx, 3**(-cx+4))
D = (dx, 3**(-dx+4))

# Confirm all on the line
for p in [A,B,C,D]:
    assert abs(p[1] - (-p[0]+k)) < 1e-8, p

# Sort by x and relabel
pts = sorted([A,B,C,D], key=lambda p: p[0])
A_,B_,C_,D_ = pts

AD = math.hypot(D_[0]-A_[0], D_[1]-A_[1])
BC = math.hypot(C_[0]-B_[0], C_[1]-B_[1])
target = 4*math.sqrt(2)
print('VERIFY_PASS' if abs(AD-BC-target) < 1e-6 else 'VERIFY_FAIL')
