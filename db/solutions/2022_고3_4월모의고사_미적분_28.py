import sympy as sp
sqrt3 = sp.sqrt(3); pi = sp.pi
x = sp.Symbol('x', positive=True)
# F1: line y=sqrt(3)x meets semicircle (x-sqrt3)^2+y^2=3
sols = sp.solve((x-sqrt3)**2 + (sqrt3*x)**2 - 3, x)
F1x = [s for s in sols if sp.simplify(s) != 0][0]
F1 = (F1x, sqrt3*F1x)
# G1: diagonal y=x/sqrt(3) meets semicircle
sols = sp.solve((x-sqrt3)**2 + (x/sqrt3)**2 - 3, x)
G1x = [s for s in sols if sp.simplify(s) != 0][0]
G1 = (G1x, G1x/sqrt3)
assert sp.simplify((F1[0]-sqrt3)**2 + F1[1]**2 - 3) == 0
assert sp.simplify((G1[0]-sqrt3)**2 + G1[1]**2 - 3) == 0
E1 = (2*sqrt3/3, 2); D1 = (2*sqrt3, 2)
def shoelace(pts):
    s=0; n=len(pts)
    for i in range(n):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
        s += x1*y2 - x2*y1
    return sp.Abs(s)/2
quad = shoelace([F1,E1,D1,G1])
sector = sp.Rational(1,2)*3*(pi/3)
tri = sp.Rational(1,2)*3*sp.sin(pi/3)
seg = sector - tri
a1 = sp.simplify(quad - seg)
# A2B2C2D2: A2 on y=x/sqrt3, D2 on circle, ratio 1:sqrt3
h = sp.Symbol('h', positive=True)
hsol = [s for s in sp.solve(3*(2*h-1)**2 + h**2 - 3, h) if sp.simplify(s)!=0][0]
scale = hsol/2
ratio = scale**2
S_inf = sp.simplify(a1/(1-ratio))
expected = sp.Rational(169,798)*(8*sqrt3 - 3*pi)
if sp.simplify(S_inf - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
