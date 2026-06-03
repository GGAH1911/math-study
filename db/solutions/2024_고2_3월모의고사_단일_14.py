import sympy as sp
k = sp.symbols('k', positive=True)
# 원래 문제의 점들
O = sp.Point(0,0)
A = sp.Point(k,0)
B = sp.Point(k, sp.sqrt(k))           # y=sqrt(x) 위
C = sp.Point(k, sp.sqrt(k*k))         # y=sqrt(kx) 위, x=k
areaOAB = sp.Triangle(O,A,B).area
areaOBC = sp.Triangle(O,B,C).area
# 조건: area(OBC) = 2 * area(OAB)
sol = sp.solve(sp.Eq(sp.Abs(areaOBC), 2*sp.Abs(areaOAB)), k)
# k>1 인 해
ks = [s for s in sol if s.is_real and s>1]
ans_area = sp.simplify(sp.Abs(areaOBC.subs(k, ks[0])))
print('VERIFY_PASS' if ans_area == 27 else 'VERIFY_FAIL')
