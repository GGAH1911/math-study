import sympy as sp

x, y, c = sp.symbols('x y c', positive=True, real=True)
# C1: focus F=(c,0), directrix x=0 -> sqrt((x-c)^2+y^2)=x
C1 = sp.Eq((x-c)**2 + y**2, x**2)
# C2: vertex F=(c,0), same directrix x=0 -> focus (2c,0), sqrt((x-2c)^2+y^2)=x
C2 = sp.Eq((x-2*c)**2 + y**2, x**2)
sol = sp.solve([C1, C2], [x, y], dict=True)
# pick the two intersection points
pts = [(s[x], s[y]) for s in sol]
# AF = 6 condition: use one with y>0
A = max(pts, key=lambda p: p[1])
B = (A[0], -A[1])
F = (c, 0)
AF = sp.sqrt((A[0]-F[0])**2 + (A[1]-F[1])**2)
c_val = sp.solve(sp.Eq(AF, 6), c)
c_val = [v for v in c_val if v.is_real and v > 0][0]
A_n = (A[0].subs(c, c_val), A[1].subs(c, c_val))
B_n = (B[0].subs(c, c_val), B[1].subs(c, c_val))
F_n = (c_val, 0)
# area via shoelace
area = sp.Rational(1,2)*abs((A_n[0]-F_n[0])*(B_n[1]-F_n[1]) - (B_n[0]-F_n[0])*(A_n[1]-F_n[1]))
area = sp.simplify(area)
expected = 8*sp.sqrt(2)
print('VERIFY_PASS' if sp.simplify(area - expected) == 0 else 'VERIFY_FAIL')
