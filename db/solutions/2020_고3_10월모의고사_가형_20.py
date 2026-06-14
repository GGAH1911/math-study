CANDIDATE = 2
import sympy as sp
x=sp.symbols('x',real=True)
# G: n=3 increasing on (-inf,-1)
f3=3*x/(x**3+1); d3=sp.diff(f3,x)
G=all(float(d3.subs(x,t))>0 for t in [-10,-3,-1.5,-1.05])
# L: continuity n, then count distinct real roots of f=2
ns=[n for n in range(1,12) if sp.limit(n*x/(x**n+1),x,-1)==-2]
L=False
if ns==[4]:
    rts=sp.solve(sp.Eq(4*x/(x**4+1),2),x)
    rr=[r for r in rts if r.is_real]
    L=(len(set(rr))==2)
# D: sum of n<=10 with local min on (-1,inf) equals 24?
good=[]
for n in range(1,11):
    f=n*x/(x**n+1); d2=sp.diff(f,x,2)
    crit=sp.solve(sp.numer(sp.together(sp.diff(f,x))),x)
    hasmin=False
    for c in crit:
        cv=complex(c.evalf())
        if abs(cv.imag)<1e-9 and cv.real>-1 and float(d2.subs(x,cv.real))>1e-9:
            hasmin=True
    if hasmin: good.append(n)
D=(sum(good)==24)
truth={'G':G,'L':L,'D':D}
choice_sets={1:{'G'},2:{'G','L'},3:{'G','D'},4:{'L','D'},5:{'G','L','D'}}
correct={k for k,v in truth.items() if v}
ans=[k for k,s in choice_sets.items() if s==correct]
print('VERIFY_PASS' if (ans==[CANDIDATE]) else 'VERIFY_FAIL')
