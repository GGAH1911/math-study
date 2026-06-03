import sympy as sp
t, s, a = sp.symbols('t s a', real=True)
v = 3*t*(a - t)
# 위치 x(t) = 16 + integral of v from 0 to t
x = 16 + sp.integrate(v.subs(t, s), (s, 0, t))
# x(2a) = 0 조건으로 a 결정
sol = sp.solve(sp.Eq(x.subs(t, 2*a), 0), a)
a_val = [r for r in sol if r.is_real and r > 0][0]
v_a = v.subs(a, a_val)
# |v| 적분으로 0~5 거리 계산
dist = sp.integrate(sp.Abs(v_a), (t, 0, 5))
print('VERIFY_PASS' if sp.simplify(dist - 58) == 0 else 'VERIFY_FAIL')
