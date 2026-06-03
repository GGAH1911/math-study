import math

def bisect(f, a, b, tol=1e-13, n=300):
    fa, fb = f(a), f(b)
    if fa*fb > 0: raise ValueError('no sign change')
    for _ in range(n):
        m = 0.5*(a+b)
        fm = f(m)
        if abs(fm) < tol or (b-a) < tol: return m
        if fa*fm < 0: b, fb = m, fm
        else: a, fa = m, fm
    return 0.5*(a+b)

log2 = math.log2

def find_x2(x1):
    y1 = log2(x1)
    f = lambda x: 2**x + x - (x1 + y1)
    return bisect(f, -20.0, 30.0)

def find_x3(slope):
    f = lambda x: slope*x - 2**(-x)
    return bisect(f, 1e-10, 60.0)

def tri_area(p, q):
    return abs(p[0]*q[1] - p[1]*q[0]) / 2.0

def residual(x1):
    y1 = log2(x1)
    x2 = find_x2(x1)
    y2 = 2**x2
    slope = y2/x2
    x3 = find_x3(slope)
    y3 = 2**(-x3)
    A, B, C = (x1,y1), (x2,y2), (x3,y3)
    return tri_area(A,B) - 2*tri_area(A,C)

x1 = bisect(residual, 1.0001, 5.0)
y1 = log2(x1)
x2 = find_x2(x1)
y2 = 2**x2
slope = y2/x2
x3 = find_x3(slope)
y3 = 2**(-x3)

A, B, C = (x1,y1), (x2,y2), (x3,y3)

assert x1 > 1, 'x1>1 fail'
assert abs(tri_area(A,B) - 2*tri_area(A,C)) < 1e-8, 'area cond fail'

OA = math.hypot(x1, y1)
OC = math.hypot(x3, y3)

g = abs(OC - OA/2) < 1e-6
n = abs((x2 + y1) - 4*x3) < 1e-6
d = abs(slope - 3*(0.5)**(1.0/3.0)) < 1e-6

print('VERIFY_PASS' if (g and n and d) else 'VERIFY_FAIL')