from sympy import *
x = symbols('x')
f = x**2*(x-3)*(x-5) + Rational(1,2)*x
# 1) 원점 접선 조건
g = f - Rational(1,2)*x
assert g.subs(x,0)==0 and diff(g,x).subs(x,0)==0, 'tangent fail'
# 2) A,B 교점 확인
roots_g = solve(g, x)
assert set([r for r in roots_g if r>0]) == {3,5}, 'intersection fail'
# 3) AB 거리
xA,xB = 3,5
yA,yB = Rational(1,2)*xA, Rational(1,2)*xB
AB = sqrt((xB-xA)**2+(yB-yA)**2)
assert AB==sqrt(5), 'AB fail'
# 4) S1=S2
S1 = integrate(g,(x,0,3))
S2 = -integrate(g,(x,3,5))
assert S1==S2, 'area fail'
# 5) f(1)
val = f.subs(x,1)
if val == Rational(17,2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', val)