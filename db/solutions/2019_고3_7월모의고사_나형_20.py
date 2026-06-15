import sympy as sp
import numpy as np

x = sp.symbols('x', real=True)
a, b, c = sp.symbols('a b c', real=True)
f = a*x**4 + b*x**2 + c
fp = sp.diff(f, x)
# (가) even quartic with exactly 3 distinct real roots forces x=0 root => c=0; (나) f(1)=-3/4, f'(-1)=1
sol = sp.solve([sp.Eq(c,0), sp.Eq(f.subs(x,1), sp.Rational(-3,4)), sp.Eq(fp.subs(x,-1),1)], [a,b,c], dict=True)[0]
A,B,C = sol[a], sol[b], sol[c]
F = A*x**4 + B*x**2 + C
Fp = sp.diff(F, x)
ok = (A>0)
rts = sorted({r for r in sp.solve(sp.Eq(F,0), x) if r.is_real}, key=lambda r: float(r))
ok = ok and (len(rts)==3)
alpha = rts[0]
# G1: f(0)=0
g1 = sp.simplify(F.subs(x,0))==0
# G2: f'(alpha)=-4
g2 = sp.simplify(Fp.subs(x,alpha))==-4
# G3: count distinct real roots of |f(x)|=k(x-alpha)
Af,Bf,Cf,al = float(A),float(B),float(C),float(alpha)
def Fval(t): return Af*t**4+Bf*t**2+Cf
def count_roots(kv):
    s=set()
    for sign in (1,-1):
        poly=[Af,0.0,Bf,-sign*kv,Cf+sign*kv*al]
        for r in np.roots(poly):
            if abs(r.imag)<1e-7:
                xr=r.real; fv=Fval(xr)
                if (sign==1 and fv>=-1e-6) or (sign==-1 and fv<=1e-6):
                    s.add(round(xr,5))
    return len(s)
lo=8.0/27.0
expect={0.20:5, lo+0.03:3, 2.0:3, 3.9:3, 4.1:2, 6.0:2}
g3_count = all(count_roots(kv)==ev for kv,ev in expect.items())
t,k = sp.symbols('t k', real=True)
tang = sp.solve([sp.Eq(-F.subs(x,t), k*(t-alpha)), sp.Eq(-Fp.subs(x,t), k)], [t,k], dict=True)
kset = {sp.nsimplify(s_[k]) for s_ in tang if s_[t].is_real and 0<float(s_[t])<2}
lower_ok = sp.Rational(8,27) in kset
upper_ok = sp.Abs(Fp.subs(x,alpha))==4
g3 = g3_count and lower_ok and upper_ok
statements=(bool(g1),bool(g2),bool(g3))
option={(True,False,False):1,(True,True,False):2,(True,False,True):3,(False,True,True):4,(True,True,True):5}.get(statements)
print('f=',F,'roots=',rts)
print('statements=',statements,'option=',option)
print('VERIFY_PASS' if (ok and option==5) else 'VERIFY_FAIL')
