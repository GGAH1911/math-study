import sympy as sp
t=sp.symbols('t')
v=3*t**2-11*t+8
# ㄱ: 방향이 t=1에서 바뀌는가
v1=v.subs(t,1)
left=v.subs(t,sp.Rational(9,10))
right=v.subs(t,sp.Rational(11,10))
g1 = (v1==0) and (left>0) and (right<0)
# ㄴ: a(t)=1 되는 t에서 위치=2
a=sp.diff(v,t)
t_n=sp.solve(a-1,t)[0]
x=sp.integrate(v,(t,0,t_n))
g2 = (x==2)
# ㄷ: t=0~2 거리 = 6 ?
d=sp.integrate(sp.Abs(v),(t,0,2))
g3 = (sp.simplify(d-6)==0)
true_set={'ㄱ':g1,'ㄴ':g2,'ㄷ':g3}
selected={'ㄱ':True,'ㄴ':True,'ㄷ':False}
ok = all(true_set[k]==selected[k] for k in ['ㄱ','ㄴ','ㄷ'])
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')