import sympy as sp
# P 위치 x=1-cos(4t), y=(1/4)sin(4t). 속력 최대일 때 가속도 크기.
# 파라미터화: 각진동수 w, y진폭 A.  속력²=A²w²cos²+w²sin²... 최대는 sin(wt)=±1 → cos(wt)=0.
t = sp.symbols('t', real=True)
w = 4
x = 1 - sp.cos(w*t)
y = sp.Rational(1,4)*sp.sin(w*t)
CANDIDATE = 4
vx, vy = sp.diff(x,t), sp.diff(y,t)
ax, ay = sp.diff(x,t,2), sp.diff(y,t,2)
speed2 = sp.simplify(vx**2 + vy**2)
# 속력² 를 c=cos(wt)로 보면 단조 → 최대점은 sin(wt)=±1 (cos(wt)=0)
sol = sp.solve(sp.Eq(sp.cos(w*t), 0), t)
tmax = sol[0]
amag = sp.simplify(sp.sqrt(ax**2 + ay**2).subs(t, tmax))
print('VERIFY_PASS' if sp.nsimplify(amag) == CANDIDATE else 'VERIFY_FAIL')
