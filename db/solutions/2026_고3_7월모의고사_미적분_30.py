# (f(x))^3+f(x) = a/(x^2+12) - bx - 16b/3.  g(y)=y^3+y 가 증가라 f 는 우변과 증감이 같다.
# 역함수 존재(단조) + f'(k)=0 → 우변'(x) = -2ax/(x^2+12)^2 - b 가 항상 ≤0 이고 x=k 에서만 0.
#   즉 b = max_x(-2ax/(x^2+12)^2), 그 최대점이 k.
# 교점: g(f(x))=g(-bx) → a/(x^2+12) - 16b/3 + b^3x^3 = 0. 정리하면 x^2(...) 꼴이라
#   x=0 (중근) 과 실근 하나뿐인 삼차식이 남고, 그 실근이 k+8 이어야 한다.
CANDIDATE = 59
import sympy as sp

x = sp.symbols('x', real=True)
a, b = sp.symbols('a b', positive=True)
u = -2*a*x/(x**2 + 12)**2                       # 우변의 도함수에서 b 를 뺀 부분
k = [c for c in sp.solve(sp.diff(u, x), x) if c.is_real and c < 0][0]
assert sp.simplify(k + 2) == 0                  # k = -2
b_of_a = sp.simplify(u.subs(x, k))              # b = a/64
a_of_b = sp.solve(sp.Eq(b, b_of_a), a)[0]
eq = sp.together((a/(x**2 + 12) - sp.Rational(16, 3)*b + b**3*x**3).subs(a, a_of_b))
poly = sp.expand(sp.numer(eq))
cubic = sp.simplify(sp.cancel(poly/x**2))       # x=0 중근 제거
b0 = [v for v in sp.solve(sp.Eq(cubic.subs(x, k + 8), 0), b) if v.is_real and v > 0][0]
val = sp.nsimplify(sp.simplify(a_of_b.subs(b, b0)*b0))
q, p = sp.fraction(val)
print('VERIFY_PASS' if sp.Integer(p + q) == CANDIDATE and sp.gcd(p, q) == 1 else 'VERIFY_FAIL')
