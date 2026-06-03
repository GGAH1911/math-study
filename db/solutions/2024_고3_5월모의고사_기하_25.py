import sympy as sp
x1, y1 = sp.symbols('x1 y1', positive=True)
# 원래 타원
ellipse = sp.Eq(x1**2/2 + y1**2, 1)
# 초점: a^2=2, b^2=1 => c=1
c = sp.sqrt(2-1)
# 접선 기울기 (음함수 미분 x + 2 y y' = 0)
m_t = -x1/(2*y1)
# PF 기울기
m_pf = y1/(x1 - c)
cond = sp.Eq(m_t*m_pf, 1)
sols = sp.solve([ellipse, cond], [x1, y1], dict=True)
ok = False
for s in sols:
    xv, yv = s[x1], s[y1]
    if xv > 0 and yv > 0 and sp.simplify(xv - c) != 0:
        val = sp.simplify(xv**2 + yv**2)
        if sp.simplify(val - sp.Rational(11,9)) == 0:
            ok = True
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
