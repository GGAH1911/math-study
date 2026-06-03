import sympy as sp
x, a, c = sp.symbols('x a c', real=True)
# f: vertex A=(2,a), through O
p = -a/4
f = p*(x-2)**2 + a
assert sp.simplify(f.subs(x,0)) == 0
# g: vertex C=(0,c) on y-axis, leading coef negative, passes B(2,0) and D(-2,0)
q = c/4
g = -q*x**2 + c
assert sp.simplify(g.subs(x,2)) == 0
assert sp.simplify(g.subs(x,-2)) == 0
# Quadrilateral OABC area via shoelace
pts = [(0,0),(2,a),(2,0),(0,c)]
s = 0
for i in range(4):
    x1,y1 = pts[i]; x2,y2 = pts[(i+1)%4]
    s += x1*y2 - x2*y1
area = sp.Abs(s)/2
eq1 = sp.Eq(area, 9)
# Line OA: y=(a/2)x; Line BC through B(2,0),C(0,c): y = -c/2*(x-2)
OA = (a/2)*x
BC = -c/2*(x-2)
# E is intersection of OA and BC with x-coordinate -2 (foot D=(-2,0))
eq2 = sp.Eq(OA.subs(x,-2), BC.subs(x,-2))
sols = sp.solve([eq1, eq2], [a, c], dict=True)
ok = False
for sol in sols:
    av, cv = sol[a], sol[c]
    if av < 0 and cv > 0:
        val = sp.simplify(f.subs({a:av, x:-4}) + g.subs({c:cv, x:-4}))
        if val == 39:
            ok = True
            break
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
