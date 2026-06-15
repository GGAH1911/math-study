import sympy as sp
# f 최고차1 삼차, g(t)=(f(t)-f(0))/t=t²+bt+c. (가) g 최솟값 0. (나) f'(x)=g(a)의 근 a,5/3 (a>5/3).
# A_m={x|f'(x)=g(m), 0<x<=m}. n(A_m)=2 인 자연수 m 의 합?
CANDIDATE = 35
a, b = sp.symbols('a b', real=True)
c = b**2/4                                   # g 최솟값 0 → c=b²/4
ga = (a + b/2)**2                            # g(a)=(a+b/2)²
sols = sp.solve([sp.Eq(a + sp.Rational(5, 3), -2*b/3),     # 근의 합
                 sp.Eq(a*sp.Rational(5, 3), (c - ga)/3)],  # 근의 곱
                [a, b], dict=True)
pick = [s for s in sols if s[a] > sp.Rational(5, 3)][0]    # a=5, b=-10
bv, cv = pick[b], pick[b]**2/4               # b=-10, c=25
x = sp.Symbol('x')
total = 0
for m in range(1, 30):
    k = (m + bv/2)**2                        # g(m)
    roots = sp.solve(sp.Eq(3*x**2 + 2*bv*x + cv, k), x)   # f'(x)=g(m)
    cnt = len({r for r in roots if r.is_real and 0 < r <= m})
    if cnt == 2:
        total += m
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL')
