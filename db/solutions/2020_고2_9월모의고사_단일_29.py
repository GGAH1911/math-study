import sympy as sp
# y=a^x, y=log_a x (y=x 대칭). 직선 y=-x+t 와 만나는 A=(p,q),B=(q,p), q=a^p. H=(p,0).
# (가) OH:AB=1:2 → q=(1+√2)p.  (나) 외접원 R=√2/2 → p²+q²=p+q. 200(t-a)?
CANDIDATE = 50
p = sp.symbols('p', positive=True)
q = (1+sp.sqrt(2))*p
pv = [x for x in sp.solve(sp.Eq(p**2+q**2, p+q), p) if x > 0][0]   # 1/2
qv = q.subs(p, pv)
av = qv**(1/pv)                                              # a^p=q → a=q^(1/p)
tv = pv + qv                                                 # t=p+q
print('VERIFY_PASS' if sp.simplify(200*(tv-av) - CANDIDATE) == 0 else 'VERIFY_FAIL')
