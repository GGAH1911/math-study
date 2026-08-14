# f(x)=3x^2+4 의 부정적분 F, F(0)+F(2)=14 → F(3)?
# F(x)=x^3+4x+C 로 두고 C 를 조건에서 실제로 풀어 F(3) 을 구한 뒤 CANDIDATE 와 비교.
CANDIDATE = 38
import sympy as sp

x, C = sp.symbols('x C')
f = 3*x**2 + 4
F = sp.integrate(f, x) + C                    # 부정적분 + 적분상수
C0 = sp.solve(sp.Eq(F.subs(x, 0) + F.subs(x, 2), 14), C)[0]
val = sp.simplify(F.subs({x: 3, C: C0}))
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
