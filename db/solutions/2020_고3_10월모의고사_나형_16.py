from sympy import *
CANDIDATE=Rational(-4,3)
x,t=symbols('x t')
A,C=symbols('A C')
g=x**2+2*A*x+C
eq1=Eq(A,integrate(g.subs(x,t),(t,0,1)))
eq2=Eq(g.subs(x,0)-A,Rational(2,3))
sol=solve([eq1,eq2],[A,C])
gg=g.subs(sol)
val=simplify(gg.subs(x,1))
print('VERIFY_PASS' if val==CANDIDATE else 'VERIFY_FAIL')