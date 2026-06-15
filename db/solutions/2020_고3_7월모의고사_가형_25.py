import sympy as sp
# x=3t-(2/π)cosπt, y=6lnt-(2/π)sinπt. t=1/2 에서 속력?
CANDIDATE = 13
t = sp.symbols('t', positive=True)
x = 3*t - sp.Rational(2,1)/sp.pi*sp.cos(sp.pi*t)
y = 6*sp.ln(t) - sp.Rational(2,1)/sp.pi*sp.sin(sp.pi*t)
sp_ = sp.sqrt(sp.diff(x,t)**2 + sp.diff(y,t)**2).subs(t, sp.Rational(1,2))
print('VERIFY_PASS' if sp.simplify(sp_ - CANDIDATE) == 0 else 'VERIFY_FAIL')
