import sympy as sp
# f(x)=6πx³+px²+qx+r, g(x)=1/(2+sin f(x)). 조건으로 p,q,r 결정 후 a²=(g'(-1/2)/π)².
# (가) α1=0 극점·g(0)=2/5 → sin f(0)=1/2, 0<f(0)<π/2 → f(0)=π/6=r. α1=0 극점 → f'(0)=0 → q=0.
#   g'=0 ⟺ f'=0(x=0, x2=-p/9π) 또는 cos f=0.
# (나) sin f(α5)-sin f(α2)=1/2.  구조: α2,3,4=cos f=0(sin=-1,+1,-1), α5=x2(극소,sin f(x2)=-1/2).
#   ⟹ f(x2)=-17π/6 → p³/(243π²)+π/6=-17π/6 → p=-9π.
x = sp.symbols('x')
CANDIDATE = 27
p = sp.solve(sp.Eq(sp.Symbol('P')**3/(243*sp.pi**2) + sp.pi/6, -sp.Rational(17,6)*sp.pi),
             sp.Symbol('P'))
p = [s for s in p if s.is_real][0]               # = -9π
f = 6*sp.pi*x**3 + p*x**2 + sp.pi/6
g = 1/(2 + sp.sin(f))
a = sp.simplify(sp.diff(g, x).subs(x, sp.Rational(-1, 2)) / sp.pi)   # g'(-1/2)=aπ
print('VERIFY_PASS' if sp.simplify(a**2) == CANDIDATE else 'VERIFY_FAIL')
